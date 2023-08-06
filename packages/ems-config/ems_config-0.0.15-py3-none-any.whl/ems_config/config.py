import io
import os
import requests

from pathlib import Path
from shutil import copyfile
from ems_config.vars import APP_DATA_DIR
from ems_config.helpers import get_from_app_data


def _read(f, path):
    # We let the user handle exceptions
    if path.endswith("yml"):
        import yaml
        return yaml.safe_load(f)
    if path.endswith("json"):
        import json
        return json.loads(f.read())
    if path.endswith("ini"):
        from configparser import ConfigParser
        cp = ConfigParser()
        cp.read_file(f, path)
        return cp
    raise ValueError(f"Unknown config extension: {path}")


def read_file(path):
    if isinstance(path, Path):
        path = str(path)
    with open(path, 'r') as f:
        return _read(f, path)


def parse_config(config_template=None, config_path=None):
    os.makedirs(APP_DATA_DIR, exist_ok=True)

    if config_template is None:
        if "CONFIG_TEMPLATE_PATH" in os.environ:
            config_template = os.getenv("CONFIG_TEMPLATE_PATH")
        else:
            config_template = "config.example.ini"

    if config_path is None:
        if "CONFIG_PATH" in os.environ:
            config_path = os.getenv("CONFIG_PATH")
        else:
            template_filename = os.path.basename(config_template)
            config_path = get_from_app_data(template_filename.replace(".example", ""))

    if not os.path.exists(config_path):
        dirname = os.path.dirname(config_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)

        copyfile(config_template, config_path)

    cfg = read_file(config_path)

    return cfg


def parse_remote_config(url="https://assets.ems.vestas.net/config.ini", verify=False):
    config_data = requests.get(url, verify=verify).text
    return _read(io.StringIO(config_data), url)
