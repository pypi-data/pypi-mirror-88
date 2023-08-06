from .pkcs12_certificate import Pkcs12Certificate


class Pkcs12GenerationResult(object):

    def __init__(self, model):
        self.__pfx = None

        if model is not None:
            if model.get('pfx', None) is not None:
                self.__pfx = Pkcs12Certificate(model.get('pfx'))

    @property
    def pfx(self):
        return self.__pfx

    @pfx.setter
    def pfx(self, value):
        self.__pfx = value


__all__ = ['Pkcs12GenerationResult']
