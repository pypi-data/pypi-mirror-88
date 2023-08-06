# Handles fetching of meta data
import os
from functools import reduce
from operator import getitem

import yaml


def update_line_in_file(replace_containing, replace_with, filename):
    f = open(filename, 'r')
    lines = f.readlines()
    lines_upd = [f"{replace_with}\n" if replace_containing in l else l for l in lines]
    f.close()
    with open(filename, 'w') as f:
        f.write(''.join(lines_upd))
        f.close()


def get_version():
    PKG_DIR = os.path.dirname(__file__)
    v = open(f'{PKG_DIR}/data/VERSION').readlines()[0]
    return v.ljust(10, ' ')


def get_amz_config(key_chain):

    HOME_DIR = os.environ["HOME"]
    AMZ_CONFIG_FILE = HOME_DIR + '/.amz/data/amz-config.yaml'
    try:
        config = yaml.load(open(AMZ_CONFIG_FILE, 'r'), Loader=yaml.FullLoader)
        return reduce(getitem, key_chain, config)
    except:
        return


def get_yaml_config(filepath, key_chain):

    try:
        config = yaml.load(open(filepath, 'r'), Loader=yaml.FullLoader)
        return reduce(getitem, key_chain, config)
    except:
        return


def highlight_cmd(cmd):
    return f'\033[90m\033[107m {cmd} \033[0m'
