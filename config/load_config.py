import os
import yaml

from loguru import logger
from models import Config


def load_config() -> Config:
    settings_path = os.path.join(os.path.dirname(__file__), "settings.yaml")
    variables = (
        "eth_rpc",
        "op_rpc",
        "bsc_rpc",
        "polygon_rpc",
        "zk_era_rpc",
        "arb_rpc",
        "avax_rpc",
        "base_rpc",
        "max_priority_fee_per_gas",
    )

    if not os.path.exists(settings_path):
        logger.error(
            f"Config file not found. Please create a config.yaml file in the config directory."
        )
        exit(1)

    if not all(
        variable in yaml.safe_load(open(settings_path)) for variable in variables
    ):
        logger.error(
            f"Config file is missing some variables. Please check the settings.yaml file in the config directory."
        )
        exit(1)

    with open(settings_path) as file:
        config = yaml.safe_load(file)

    return Config(**config)
