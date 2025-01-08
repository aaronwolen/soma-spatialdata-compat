import json
from pathlib import Path


def load_config(config_path="config.json"):
    with open(config_path, "r") as f:
        config = json.load(f)
    return config


def get_data_dir(config):
    data_dir = Path(config["data_dir"])
    if not data_dir.exists():
        data_dir.mkdir()
    return data_dir


def get_dataset(config):
    return config["datasets"][0]
