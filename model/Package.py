from tools.crypto import calc_md5, calc_hmac
from tools.strtool import strcat
from tools.time import get_timestamp


class OPTPackage:
    H = calc_md5
    MAC = calc_hmac
    def __init__(self, **kwargs):
        self.datahash = kwargs.get('datahash')
        self.sessionid = kwargs.get('sessionid')
        self.timestamp = kwargs.get('timestamp')
        self.pvf = kwargs.get('pvf')
        self.opv = kwargs.get('opv')
        self.R = kwargs.get('path')
        self.payload = kwargs.get('payload')

    def __repr__(self):
        class_name = self.__class__.__name__
        attributes = ', '.join(f'{key}={value}' for key, value in self.__dict__.items())
        return f'{class_name}({attributes})'

    def initialization(self, PK, Ki, Kd, PATH, payload):
        self.R = PATH
        self.payload = payload
        self.datahash = self.H(str(payload))
        self.timestamp = get_timestamp()
        self.sessionid = self.H(strcat(PK, self.R, self.timestamp))
        self.pvf = self.MAC(Kd, self.datahash)
        pvf = self.pvf
        self.opv = [0 for i in range(len(self.R) + 1)]
        Ki.append(Kd)
        for i, pa in enumerate(self.R, 1):
            self.opv[i] = self.MAC(Ki[i], strcat(pvf, self.datahash, self.R[i - 1], self.timestamp))
            pvf = self.MAC(Ki[i], self.pvf)
        self.t = get_timestamp()

    def R_validation(self, Ki, i):
        opv_ = self.MAC(Ki, strcat(self.pvf, self.datahash, self.R[i - 1], self.timestamp))
        if self.opv[i] == opv_:
            self.pvf = self.MAC(Ki, self.pvf)
            self.forward(self.R[i + 1])
        else:
            self.drop()

    def D_validation(self, Ki, Kd):
        K_ = Kd + Ki
        pvf_ = self.datahash
        for i in K_:
            pvf_ = self.MAC(i, pvf_)
        opv_ = self.MAC(Kd, strcat(self.pvf, self.datahash, self.R[len(self.R) - 1], self.timestamp))
        if (pvf_ == self.pvf and opv_ == self.opv[-1]):
            self.succeed()
        else:
            self.drop()

    def forward(self):
        ...

    def drop(self):
        ...

    def succeed(self):
        ...
