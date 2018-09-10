import os

from ruamel import yaml

TOKEN = 'token'

__config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
config = dict()

def save():
    stream = open(__config_file, 'w')
    res = yaml.round_trip_dump(config, indent=2, block_seq_indent=1)

    stream.write(res)
    stream.close()


def load():
    if not os.path.exists(__config_file):
        set_defaults()
        save()
        return

    global config
    
    stream = open(__config_file, 'r')
    config = yaml.round_trip_load(stream)
    stream.close()


def set_defaults():
    pass
