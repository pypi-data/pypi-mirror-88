import base64
import binascii
import os

from .pkcs12_generation_result import Pkcs12GenerationResult
from .pki_express_config import PkiExpressConfig
from .pki_express_operator import PkiExpressOperator


class Pkcs12Generator(PkiExpressOperator):
    def __init__(self, config=None):
        if not config:
            config = PkiExpressConfig()
        super(Pkcs12Generator, self).__init__(config)
        
        self.__key = None
        self.__cert_file_path = None
        self.__password = None
        
    @property
    def key(self):
        return self.__key
    
    @key.setter
    def key(self, value):
        self.__key = value
        
    @property
    def cert_file_path(self):
        return self.__cert_file_path

    # region set_cert_file

    def set_cert_file_from_path(self, path):
        if not path and not os.path.exists(path):
            raise Exception('The provided certificate file was not found')
        self.__cert_file_path = path

    def set_cert_file_from_raw(self, content_raw):
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self.__cert_file_path = temp_file_path

    def set_cert_file_from_base64(self, content_base64):
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided certificate is not Base64-encoded')
        self.set_cert_file_from_raw(raw)

    # endregion
        
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, value):
        self.__password = value

    def generate(self, password=None):
        if self.__key is None:
            raise Exception('The generated key was not set')

        if self.__cert_file_path is None:
            raise Exception('The certificate file was not set')

        args = [self.__key, self.__cert_file_path]
        if password is not None:
            args.append('--password')
            args.append(password)

        # This operation can only be used on version greater than 1.11 of the
        # PKI Express.
        self._version_manager.require_version('1.11')

        # Invoke command.
        response = self._invoke(self.COMMAND_CREATE_PFX, args)
        output = Pkcs12Generator._parse_output(response[0])
        return Pkcs12GenerationResult(output)


__all__ = ['Pkcs12Generator']
