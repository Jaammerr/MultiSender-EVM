import os
import sys
import inquirer

from inquirer.themes import GreenPassion
from art import tprint

from config.variables import CHAIN_SYMBOLS, CHAINS
from models import Account, AccountsData
from colorama import Fore

sys.path.append(os.path.realpath("."))


class Console:
    def __init__(self):
        self.accounts_data = AccountsData()

    @staticmethod
    def show_dev_info():
        os.system("cls")
        tprint("JamBit")
        print("\033[36m" + "VERSION: " + "\033[34m" + "1.0" + "\033[34m")
        print(
            "\033[36m" + "Channel: " + "\033[34m" + "https://t.me/JamBitPY" + "\033[34m"
        )
        print(
            "\033[36m"
            + "GitHub: "
            + "\033[34m"
            + "https://github.com/Jaammerr"
            + "\033[34m"
        )
        print(
            "\033[36m"
            + "DONATION EVM ADDRESS: "
            + "\033[34m"
            + "0x08e3fdbb830ee591c0533C5E58f937D312b07198"
            + "\033[0m"
        )
        print()

    @staticmethod
    def prompt(data: list):
        answers = inquirer.prompt(data, theme=GreenPassion())
        return answers

    def get_source_chain(self):
        questions = [
            inquirer.List(
                "source_chain",
                message=Fore.LIGHTBLACK_EX + "Select source chain",
                choices=CHAINS,
            ),
        ]

        answers = self.prompt(questions)
        source_chain = answers.get("source_chain")
        self.accounts_data.source_chain = source_chain

    def get_destination_chain(self):
        destination_chains = CHAINS.copy()
        destination_chains.remove(self.accounts_data.source_chain)

        questions = [
            inquirer.List(
                "destination_chain",
                message=Fore.LIGHTBLACK_EX + "Select destination chain",
                choices=destination_chains,
            ),
        ]

        answers = self.prompt(questions)
        destination_chain = answers.get("destination_chain")
        self.accounts_data.destination_chain = destination_chain

    def verify_chains(self):
        self.get_source_chain()
        self.get_destination_chain()

        os.system("cls")
        self.show_dev_info()

        questions = [
            inquirer.List(
                "verify_chains",
                message=Fore.LIGHTBLACK_EX
                + f"Are you sure you want to bridge from {self.accounts_data.source_chain} to {self.accounts_data.destination_chain}",
                choices=["Yeah, continue", "Change"],
            ),
        ]
        answers = self.prompt(questions)

        if answers.get("verify_chains") == "Change":
            self.verify_chains()

    def get_amount_to_bridge(self) -> float:
        symbol = CHAIN_SYMBOLS.get(self.accounts_data.source_chain)

        questions = [
            inquirer.Text(
                "amount",
                message=Fore.LIGHTBLACK_EX
                + f"Enter the amount of {symbol} you want to bridge",
            ),
        ]

        answers = self.prompt(questions)
        amount = answers.get("amount")

        try:
            amount = float(amount)
            if amount <= 0:
                print(Fore.RED + ">> Invalid amount. Please enter a valid number.")
                self.get_amount_to_bridge()

            self.accounts_data.bridge_amount = amount
            return amount

        except ValueError:
            print(Fore.RED + ">> Invalid amount. Please enter a valid number")
            self.get_amount_to_bridge()

    def get_wallet(self):
        questions = [
            inquirer.Text(
                "wallet",
                message=Fore.LIGHTBLACK_EX
                + f"Enter your wallet mnemonic or private key (0x)",
            ),
        ]

        answers = self.prompt(questions)
        wallet = answers.get("wallet")

        if not wallet.startswith("0x") or len(wallet.split(" ")) < 12 > 24:
            print(
                Fore.RED
                + ">> Invalid wallet. Please enter a valid mnemonic or private key."
            )
            self.get_wallet()

        if wallet.startswith("0x"):
            self.accounts_data.private_key = wallet
        else:
            self.accounts_data.mnemonic = wallet

    def get_sub_accounts_format(self) -> str:
        questions = [
            inquirer.List(
                "sub_accounts_format",
                message=Fore.LIGHTBLACK_EX + f"Select the format of your sub-accounts",
                choices=[
                    "Addresses with static amount",
                    "Addresses with dynamic amounts",
                ],
            ),
        ]

        answers = self.prompt(questions)
        sub_accounts_format = answers.get("sub_accounts_format")
        return sub_accounts_format

    def get_sub_accounts(self, sub_accounts_format: str):
        if sub_accounts_format == "Addresses with static amount":
            if (
                not self.accounts_data.bridge_amount
                or self.accounts_data.bridge_amount <= 0
            ):
                bridge_amount = self.get_amount_to_bridge()
            else:
                bridge_amount = self.accounts_data.bridge_amount

            print("| |")
            print("| |")
            addresses = str(
                input(
                    Fore.LIGHTBLACK_EX
                    + "[?] Drop the TXT file with the sub-accounts in the format: address\n| |\n| |\n-->  "
                )
            )

        else:
            bridge_amount = None
            addresses = str(
                input(
                    Fore.LIGHTBLACK_EX
                    + "[?] Drop the TXT file with the sub-accounts in the format: address, amount\n| |\n| |\n-->  "
                )
            )

        if not os.path.exists(addresses):
            print(Fore.RED + ">> File not found. Please drop a valid TXT file.")
            self.get_sub_accounts(sub_accounts_format)

        if not os.path.isfile(addresses):
            print(Fore.RED + ">> Invalid file. Please drop a valid TXT file.")
            self.get_sub_accounts(sub_accounts_format)

        if addresses.split(".")[-1] != "txt":
            print(Fore.RED + ">> Invalid file format. Please drop a TXT file.")
            self.get_sub_accounts(sub_accounts_format)

        if not self.get_sub_accounts_txt(
            addresses,
            bridge_amount=bridge_amount,
            static=sub_accounts_format == "Addresses with static amount",
        ):
            self.get_sub_accounts(sub_accounts_format)

    def get_sub_accounts_txt(
        self, path: str, bridge_amount: float = None, static: bool = True
    ) -> bool:
        sub_accounts = []

        with open(path, "r") as file:
            for line in file.readlines():
                try:
                    if static:
                        address = line.strip()
                    else:
                        parts = line.strip().split(",")
                        address = parts[0]

                    if not address.startswith("0x") or len(address) != 42:
                        print(f">> Invalid address: {address}")
                        return False

                    amount = bridge_amount if static else float(parts[1])
                    account = Account(address=address, amount=amount)
                    sub_accounts.append(account)

                except (ValueError, IndexError):
                    print(Fore.RED + f">> Invalid sub-account format: {line}")
                    return False

        self.accounts_data.addresses = sub_accounts
        return True

    def build(self) -> AccountsData:
        self.show_dev_info()
        self.verify_chains()

        os.system("cls")
        self.show_dev_info()

        self.get_wallet()
        os.system("cls")
        self.show_dev_info()

        sub_accounts_format = self.get_sub_accounts_format()
        self.get_sub_accounts(sub_accounts_format)

        return self.accounts_data
