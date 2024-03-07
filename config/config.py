import configparser
import os
import random


def init(ininame='config/config.ini'):
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    for i in config.sections():
        for k, v in config[i].items():
            os.environ[k] = str(v)

    random.seed(int(os.getenv('RandomSeed')))

