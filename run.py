from console import Console, logger
from src.main import EVMMultiSender


def run():
    try:
        accounts_data = Console().build()
        evm = EVMMultiSender(accounts_data)
        evm.start()

    except Exception as error:
        logger.error_log(f"Failed to start the MultiSender: {error}")
        exit(1)


if __name__ == "__main__":
    run()
