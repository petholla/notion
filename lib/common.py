import os
import configparser
import logging

def get_logger():
    """Return logger with formatting."""
    logger = logging.getLogger(__file__)
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s"
    )
    return logger

def get_config_value(section, key, config_file=".credentials.ini"):
    """Get value from config file, defaults to .credentials.ini in home directory."""
    config = configparser.ConfigParser()
    home = os.path.expanduser("~")
    config = configparser.ConfigParser()
    config.read(f"{home}/{config_file}")
    return config.get(section, key)