
import configparser

CONFIG_FILE = "config.ini"

def read():
    config = configparser.ConfigParser(allow_no_value = True)
    config.read(CONFIG_FILE)
    return config

def write(config):
    with open(CONFIG_FILE, 'w+') as configfile:
        config.write(configfile)