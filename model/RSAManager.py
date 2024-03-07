import os
import random

from Crypto.PublicKey import RSA

from tools.strtool import strcat


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
    def save_keys(cls, seed, id, SK, PK):
        skdir = strcat(cls.skdir, seed)
        pkdir = strcat(cls.pkdir, seed)
        skpath = strcat(skdir, '/', id)
        pkpath = strcat(pkdir, '/', id)
        if not os.path.exists(skdir):
            os.mkdir(skdir)
        if not os.path.exists(pkdir):
            os.mkdir(pkdir)
        with open(skpath, 'wb') as f:
            f.write(SK)
        with open(pkpath, 'wb') as f:
            f.write(PK)

    @classmethod
    def load_keys(cls, seed, id):
        skpath = strcat(cls.skdir, seed, '/', id)
        pkpath = strcat(cls.pkdir, seed, '/', id)
        if not os.path.exists(skpath) or not os.path.exists(pkpath):
            SK, PK = cls.generate_key_pair()
            cls.save_keys(seed, id, SK, PK)
        else:
            with open(skpath, 'rb') as f:
                SK = f.read()
            with open(pkpath, 'rb') as f:
                PK = f.read()
        return SK, PK
