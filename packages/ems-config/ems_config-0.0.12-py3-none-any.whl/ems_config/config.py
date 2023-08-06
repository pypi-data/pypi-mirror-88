import os
from pathlib import Path
from shutil import copyfile

from ems_config.vars import APP_DATA_DIR
from ems_config.helpers import get_from_app_data


def read_file(path):
    if isinstance(path, Path):
        path = str(path)
    if path.endswith("yml"):
        with open(path, 'r') as stream:
            import yaml
            # We let the user handle exceptions
            return yaml.safe_load(stream)
    elif path.endswith("ini"):
        from configparser import ConfigParser
        cp = ConfigParser()
        cp.read(path)
        return cp
    elif path.endswith("json"):
        import json
        with open(path, 'r') as stream:
            return json.loads(stream.read())
    else:
        raise ValueError(f"Unknown config extension: {path}")


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
