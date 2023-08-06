import base64
import binascii
import os

from abc import ABCMeta, abstractmethod

from .base_signer import BaseSigner
from .pki_express_config import PkiExpressConfig


class Signer(BaseSigner):
    __metaclass__ = ABCMeta

    def __init__(self, config=None):
        if not config:
            config = PkiExpressConfig()
        super(Signer, self).__init__(config)
        self._output_file_path = None
        self._pkcs12_path = None
        self._cert_thumb = None
        self._cert_password = None
        self._trust_service_session = None
        self._key_name = None
        self._cert_file_path = None

    # region set_pkcs12

    def set_pkcs12_from_path(self, path):
        if not os.path.exists(path):
            raise Exception('The provided PKCS #12 certificate file was not '
                            'found')

        self._pkcs12_path = path

    def set_pkcs12_from_raw(self, content_raw):
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self._pkcs12_path = temp_file_path

    def set_pkcs12_from_base64(self, content_base64):
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided certificate is not Base64-encoded')
        self.set_pkcs12_from_raw(raw)

    # endregion

    @property
    def pkcs12(self):
        return self._pkcs12_path

    @property
    def output_file(self):
        return self._output_file_path

    @output_file.setter
    def output_file(self, value):
        self._output_file_path = value

    @property
    def cert_thumb(self):
        return self._cert_thumb

    @cert_thumb.setter
    def cert_thumb(self, value):
        self._cert_thumb = value

    @property
    def cert_password(self):
        return self._cert_password

    @cert_password.setter
    def cert_password(self, value):
        self._cert_password = value

    @property
    def trust_service_session(self):
        return self._trust_service_session

    @trust_service_session.setter
    def trust_service_session(self, value):
        self._trust_service_session = value

    @property
    def key_name(self):
        return self._key_name

    @key_name.setter
    def key_name(self, value):
        self._key_name = value

    @property
    def cert_file_path(self):
        return self._cert_file_path

    @cert_file_path.setter
    def cert_file_path(self, pkcs12_path):
        if not os.path.exists(pkcs12_path):
            raise Exception('The provided certificate file was not found')
        self._cert_file_path = pkcs12_path
    # end region

    @abstractmethod
    def sign(self):
        raise Exception('This method should be implemented')

    def _verify_and_add_common_options(self, args):
        # Verify and add common options between signers and signature starters.
        super(Signer, self)._verify_and_add_common_options(args)

        if not self._cert_thumb and not self._pkcs12_path and not self._trust_service_session and not self._key_name:
            raise Exception("Neither the certificate\'s thumbprint, the PKCS #12, the key name nor the "
                            "TrustServiceSession was provided")

        if self._cert_thumb:
            args.append('--thumbprint')
            args.append(self._cert_thumb)
            # This operation can only be used on versions greater than 1.3 of
            # the PKI Express.
            self._version_manager.require_version('1.3')

        if self._pkcs12_path:
            args.append('--pkcs12')
            args.append(self._pkcs12_path)
            # This operation can only be used on versions greater than 1.3 of
            # the PKI Express.
            self._version_manager.require_version('1.3')

        if self._cert_password:
            args.append('--password')
            args.append(self._cert_password)
            # This operation can only be used on versions greater than 1.3 of
            # the PKI Express.
            self._version_manager.require_version('1.3')


        if self._key_name:
            if not self._cert_file_path:
                raise Exception('The key name was passed, but no certificate file was provided.')

            args.append('--key-name')
            args.append(self._key_name)
            args.append('--cert-file')
            args.append(self._cert_file_path)

            # This operation can only be used on versions greater than 1.14 of the
            # PKI Express.
            self._version_manager.require_version('1.14')

        # Add trust service session.
        if self._trust_service_session:
            args.append('--trust-service-session')
            args.append(self._trust_service_session)
            # This option can only be used on versions greater than 1.18 of 
            # the PKI Express.
            self._version_manager.require_version('1.18')


__all__ = ['Signer']
