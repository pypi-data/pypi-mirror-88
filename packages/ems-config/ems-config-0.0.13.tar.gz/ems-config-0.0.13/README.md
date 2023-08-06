# EMS-config

This project introduces a unified way of handling config files. The philosophy is having a text-based config file
(ini, yml or toml) and then perform parsing and sanity-checking in code afterwards. Moreover, a default layout is 
encouraged.

You need to provide three paths
 1. An `app_data` directory. This is where you should put all your data and where your final config file should go.
    This is set in an environmental variable `APP_DATA_PATH`, which defaults to `app_data`.
 2. A path to your final config file. This defaults to `$APP_DATA_PATH/config.ini` if your template file is called `config.example.ini` (see below).
    That is, it strips `.example` from the filename of you template file.
 3. A path to the template file. This defaults to `config.example.ini`. 

Notice that 2 and 3 can both be set in the following parse-method or in environmental variables (`CONFIG_PATH` and `CONFIG_TEMPLATE_PATH`)
 
The assumed layout of you directory would then be something like
```
project
  - app_data/
    - config.ini
  - app.py
  - config.py
  - config.example.ini
```

Where `config.py` contains the following,

    from ems_config import parse_config
    
    config = parse_config()
    
    URL = config["DEFAULT"]["URL"]
    
and the template `config.ini.example` contains an example of the configuration,

    [DEFAULT]
    URL = http://google.com
    
You can then use the configuration in other python files like this,

    from config import URL
    print(URL)  # do stuff with the URL
    
Notice, if the `config.ini` in `app_data` (or where ever you choose to place it), the template
will be copied to that location.

## Helper methods
This library provides a few helper methods found in `ems.helpers`
```python
# Get the path of p relative to the APP_DATA_DIR
get_from_app_data(p)

## Help to parse from .ini style files
parse_dt_or_none(...)
parse_list_or_none(...)

```

## Customization
If you don't want your template to be named after the above scheme, you can pass another template
path into the `parse_config()` methods. Likewise, if you want you final config file to be located elsewhere,
you can also provide another path
```python
from ems_config import parse_config

# config_path will default to $APP_DATA_PATH/cfg.ini
config = parse_config(config_template='templates/cfg.example.ini')

config = parse_config(config_template='templates/cfg.ini', config_path='/etc/app.ini')
```