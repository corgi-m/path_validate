from random import randint, randbytes

from model.Package import OPTPackage


def package_generate(H, MAC, PK, PATH, Ki, Kd):
    package = OPTPackage()
    size = randint(1, 65535)
    payload = randbytes(size)
    package.initialization(PK=PK, Ki=Ki, Kd=Kd, PATH=PATH, payload=payload)
    return package
