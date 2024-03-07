from random import randint, randbytes

from model.Package import OPTPackage


def package_generate(PK, PATH, Ki):
    package = OPTPackage()
    size = randint(1, 65535)
    payload = randbytes(size)
    package.initialization(PK=PK, Ki=Ki, PATH=PATH, payload=payload)
    return package
