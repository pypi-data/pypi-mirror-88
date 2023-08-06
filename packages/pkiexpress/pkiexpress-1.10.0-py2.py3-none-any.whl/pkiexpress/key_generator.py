from .key_generation_result import KeyGenerationResult
from .pki_express_config import PkiExpressConfig
from .pki_express_operator import PkiExpressOperator


class SupportedKeySizes(object):
    S1024 = '1024'
    S2048 = '2048'
    S4096 = '4096'


class KeyFormats(object):
    JSON = 'json'
    BLOB = 'blob'
    XML = 'xml'


class KeyGenerator(PkiExpressOperator):

    def __init__(self, config=None):
        if not config:
            config = PkiExpressConfig()
        super(KeyGenerator, self).__init__(config)

        self.__key_size = SupportedKeySizes.S2048
        self.__key_format = KeyFormats.JSON
        self.__gen_csr = False

    @property
    def key_size(self):
        return self.__key_size

    @key_size.setter
    def key_size(self, value):
        self.__key_size = value

    @property
    def key_format(self):
        return self.__key_format

    @key_format.setter
    def key_format(self, value):
        self.__key_format = value

    @property
    def gen_csr(self):
        return self.__gen_csr

    @gen_csr.setter
    def gen_csr(self, value):
        self.__gen_csr = value

    def generate(self, key_format=None):
        key_format = key_format if (key_format is not None) else self.__key_format

        args = []
        if self.__key_size is not None:
            if self.__key_size != SupportedKeySizes.S1024 \
                    and self.__key_size != SupportedKeySizes.S2048 \
                    and self.__key_size != SupportedKeySizes.S4096:
                raise Exception('Unsupported key size: {0}'.format(self.__key_size))
            args.append('--size')
            args.append(self.__key_size)

        if self.__key_format is not None:
            args.append('--format')
            args.append(self.__key_format)

        if self.__gen_csr:
            args.append('--gen-csr')

        # This operation can only be used on version greater than 1.11 of the
        # PKI Express.
        self._version_manager.require_version('1.11')

        # Invoke command.
        response = self._invoke(self.COMMAND_GEN_KEY, args)
        output = KeyGenerator._parse_output(response[0])
        return KeyGenerationResult(output)


__all__ = ['SupportedKeySizes', 'KeyFormats', 'KeyGenerator']
