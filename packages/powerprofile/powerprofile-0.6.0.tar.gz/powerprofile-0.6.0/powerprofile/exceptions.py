# -*- coding: utf-8 -*-

class PowerProfileExceptionBaseClass(ValueError):

    def __init__(self, message=''):
        desc = ""
        self.message = message

    def __str__(self):
        return "{}: {}".format(self.desc, self.message)


class PowerProfileIncompleteCurve(PowerProfileExceptionBaseClass):

    desc = "PowerProfile Incomplete Curve"


class PowerProfileDuplicatedTimes(PowerProfileExceptionBaseClass):

    desc = "PowerProfile Duplicated Times"


class PowerProfileIncompatible(PowerProfileExceptionBaseClass):

    desc = "PowerProfile Incompatible"


class PowerProfileNotImplemented(NotImplementedError):

    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return 'Operation not implemented: ' + self.message