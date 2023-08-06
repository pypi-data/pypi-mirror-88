class KeyGenerationResult(object):

    def __init__(self, model):
        self.__key = None
        self.__csr = None

        if model is not None:
            self.__key = model.get('key', None)
            self.__csr = model.get('csr', None)

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        self.__key = value

    @property
    def csr(self):
        return self.__csr

    @csr.setter
    def csr(self, value):
        self.__csr = value


__all__ = ['KeyGenerationResult']
