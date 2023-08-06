import os
from datetime import datetime
import pytz

from ems_config.vars import APP_DATA_DIR


def parse_dt_or_none(cfg_section, key, timezone=pytz.UTC, fmt="%Y-%m-%dT%H:%M:%SZ"):
    s = cfg_section.get(key, fallback=None)
    if s is None:
        return None
    d = datetime.strptime(s, fmt)
    if timezone:
        d = d.replace(tzinfo=pytz.UTC)
    return d


def parse_list_or_none(cfg_section, key, data_type=str, delimiter=','):
    s = cfg_section.get(key, None)
    if s is None:
        return None
    return [data_type(x.strip()) for x in s.split(delimiter) if x]


def get_from_app_data(p):
    return os.path.join(APP_DATA_DIR, p)


def get_from_cfg_or_env(cfg, cfg_key, key, default, prefix_cfg=True, env_key=None):
    env_key = env_key if env_key is not None else f"{cfg_key}_{key}" if prefix_cfg else key
    try:
        return cfg[cfg_key].get(key, fallback=os.getenv(env_key, default))
    except KeyError:
        return os.getenv(env_key, default)
