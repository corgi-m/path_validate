import os
import random

from Crypto.PublicKey import RSA


class RSAManager:
    skdir = 'keys/sk/'
    pkdir = 'keys/pk/'

    @classmethod
    def generate_key_pair(cls):
        key = RSA.generate(1024, random.randbytes)
        SK = key.export_key()
        PK = key.publickey().export_key()
        return SK, PK

    @classmethod
    def save_keys(cls, seed, node_name, SK, PK):
        if not os.path.exists(cls.skdir + seed):
            os.mkdir(cls.skdir + seed)
        if not os.path.exists(cls.pkdir + seed):
            os.mkdir(cls.pkdir + seed)
        with open(cls.skdir + seed + '/' + node_name, 'wb') as f:
            f.write(SK)
        with open(cls.pkdir + seed + '/' + node_name, 'wb') as f:
            f.write(PK)

    @classmethod
    def load_keys(cls, seed, node_name):
        if not os.path.exists(cls.skdir + seed + '/' + node_name) or not os.path.exists(cls.pkdir + seed + '/' + node_name):
            SK, PK = cls.generate_key_pair()
            cls.save_keys(seed, node_name, SK, PK)
        else:
            with open(cls.skdir + seed + '/' + node_name, 'rb') as f:
                SK = f.read()
            with open(cls.pkdir + seed + '/' + node_name, 'rb') as f:
                PK = f.read()
        return SK, PK
