
import configparser

CONFIG_FILE = "config.ini"

def read():
    config = configparser.ConfigParser(allow_no_value = True)
    config.read(CONFIG_FILE)
    return config

def set_val(conf, section, option, value):
    _ensure_exists(conf, section)
    conf.set(section, option, str(value))

def _ensure_exists(conf, section):
    if not conf.has_section(section):
        conf.add_section(section)

def write(config):
    with open(CONFIG_FILE, 'w+') as configfile:
        config.write(configfile)