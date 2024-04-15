import os
import time

from colorama import Fore
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

from models import Fees, AccountsData

from config.variables import *
from console import logger


class EVMMultiSender:
    def __init__(self, data: AccountsData):
        self.input_data = data
        self.success: list[str] = []
        self.failed: list[str] = []

        self.source_chain = Web3(
            HTTPProvider(str(RPC_URLS[self.input_data.source_chain]))
        )
        if self.input_data.source_chain == "Binance Smart":
            self.source_chain.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.destination_chain = Web3(
            HTTPProvider(str(RPC_URLS[self.input_data.destination_chain]))
        )
        if self.input_data.destination_chain == "Binance Smart":
            self.destination_chain.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.wallet = (
            self.source_chain.eth.account.from_key(self.input_data.private_key)
            if self.input_data.private_key
            else self.source_chain.eth.account.from_mnemonic(self.input_data.mnemonic)
        )
        self.contract = self.source_chain.eth.contract(
            self.source_chain.to_checksum_address(
                CHAIN_CONTRACTS[self.input_data.source_chain]
            ),
            abi=SocketContracts.abi,
        )

    def get_fees(self) -> Fees:
        max_priority_fee_per_gas = self.source_chain.to_wei(
            config.max_priority_fee_per_gas, "gwei"
        )
        recommended_base_fee = (
            self.source_chain.eth.fee_history(block_count=1, newest_block="latest")
        )["baseFeePerGas"][0]
        max_fee_per_gas = recommended_base_fee + max_priority_fee_per_gas

        return Fees(
            max_priority_fee_per_gas=max_priority_fee_per_gas,
            max_fee_per_gas=max_fee_per_gas,
        )

    def get_estimate_total_cost_of_transaction(self, built_trx, fees: Fees) -> float:
        gas_estimate = self.source_chain.eth.estimate_gas(built_trx)
        total_cost = gas_estimate * (
            fees.max_fee_per_gas + fees.max_priority_fee_per_gas
        )
        total_cost_eth = self.source_chain.from_wei(total_cost, "ether")
        return total_cost_eth

    def check_if_wallet_has_enough_balance(self):
        if self.source_chain.eth.get_balance(self.wallet.address) == 0:
            logger.error_log(
                f"Wallet has no balance. Please fund your wallet. Network: {self.input_data.source_chain}"
            )
            exit(1)

        minimum_amount = sum([account.amount for account in self.input_data.addresses])
        human_balance = self.source_chain.from_wei(
            self.source_chain.eth.get_balance(self.wallet.address), "ether"
        )

        if minimum_amount > human_balance:
            logger.error_log(
                f"Wallet has not enough balance. Need at least {minimum_amount} {CHAIN_SYMBOLS[self.input_data.source_chain]}. Please fund your wallet. | Network: {self.input_data.source_chain} | Balance: {round(human_balance, 6)} {CHAIN_SYMBOLS[self.input_data.source_chain]}"
            )
            exit(1)

    def build_transaction(self, address: str, amount: float, fees: Fees):
        transaction = self.contract.functions.depositNativeToken(
            CHAIN_IDS[self.input_data.destination_chain],
            self.source_chain.to_checksum_address(address),
        )

        if self.input_data.source_chain not in ("Binance Smart", "Polygon"):
            # build EIP-1559 transaction
            built_transaction = transaction.build_transaction(
                {
                    "type": "0x2",
                    "nonce": self.source_chain.eth.get_transaction_count(
                        self.wallet.address
                    ),
                    "maxFeePerGas": fees.max_fee_per_gas,
                    "maxPriorityFeePerGas": fees.max_priority_fee_per_gas,
                    "value": self.source_chain.to_wei(amount, "ether"),
                    "chainId": CHAIN_IDS[self.input_data.source_chain],
                }
            )

        else:
            # build legacy transaction
            built_transaction = transaction.build_transaction(
                {
                    "nonce": self.source_chain.eth.get_transaction_count(
                        self.wallet.address
                    ),
                    "gas": int(
                        transaction.estimate_gas({"from": self.wallet.address}) * 1.2
                    ),
                    "gasPrice": self.source_chain.to_wei(
                        str(self.source_chain.eth.gas_price), "wei"
                    ),
                    "value": self.source_chain.to_wei(amount, "ether"),
                }
            )

        return built_transaction

    def send_transaction(self, address: str, amount: float, fees: Fees):
        try:
            built_transaction = self.build_transaction(address, amount, fees)
            signed = self.wallet.sign_transaction(built_transaction)
            tx_hash = self.source_chain.eth.send_raw_transaction(signed.rawTransaction)
            logger.info_log(
                f"Sub-account: {address} | Transaction send: {CHAINS_EXPLORERS[self.input_data.source_chain] + tx_hash.hex()} | Amount: {amount} {CHAIN_SYMBOLS[self.input_data.source_chain]} | Waiting for confirmation..\n"
            )

            receipt = self.source_chain.eth.wait_for_transaction_receipt(
                tx_hash, timeout=30
            )
            if receipt.status == 1:
                logger.success_log(
                    f"Sub-account: {address} | Transaction confirmed: {CHAINS_EXPLORERS[self.input_data.source_chain] + tx_hash.hex()} | Amount: {amount} {CHAIN_SYMBOLS[self.input_data.source_chain]}\n"
                )
                self.success.append(address)
            else:
                logger.error_log(
                    f"Sub-account: {address} | Transaction failed: {CHAINS_EXPLORERS[self.input_data.source_chain] + tx_hash.hex()} | Amount: {amount} {CHAIN_SYMBOLS[self.input_data.source_chain]}\n"
                )
                self.failed.append(address)

        except Exception as error:
            if "nonce too low" in str(error):
                time.sleep(0.25)
                self.send_transaction(address, amount, fees)

            else:
                logger.error_log(
                    f"Sub-account: {address} | Transaction failed: {error} | Amount: {amount} {CHAIN_SYMBOLS[self.input_data.source_chain]}\n"
                )
                self.failed.append(address)

    def process_transactions(self, address: str, amount: float):
        fees = self.get_fees()
        self.send_transaction(address, amount, fees)

    def export_results(self):
        try:
            results_path = os.path.join(os.getcwd().replace("src", "results"))
            os.makedirs(str(results_path), exist_ok=True)

            if self.success:
                with open(
                    os.path.join(results_path, f"success_{int(time.time())}.txt"), "w"
                ) as file:
                    file.write("\n".join(self.success))

            if self.failed:
                with open(
                    os.path.join(results_path, f"failed_{int(time.time())}.txt"), "w"
                ) as file:
                    file.write("\n".join(self.failed))

            print(Fore.LIGHTBLACK_EX + f"\n\n>> Logs exported to <<results>> folder <<")

        except Exception as error:
            logger.error_log(f"Error while exporting results: {error}")

    def start(self):
        os.system("cls")
        print(
            Fore.CYAN
            + f">>- MultiSender started | {self.input_data.source_chain} > {self.input_data.destination_chain} | Loaded {len(self.input_data.addresses)} sub-accounts -<<\n\n"
        )
        self.check_if_wallet_has_enough_balance()

        for account in self.input_data.addresses:
            self.process_transactions(account.address, account.amount)

        self.export_results()
        print(
            Fore.CYAN
            + f">>- MultiSender finished | Success: {len(self.success)} | Failed: {len(self.failed)} -<<\n"
        )
