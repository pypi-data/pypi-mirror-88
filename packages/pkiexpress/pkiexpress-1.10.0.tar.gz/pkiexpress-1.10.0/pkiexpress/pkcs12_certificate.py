import base64


class Pkcs12Certificate(object):

    def __init__(self, pfx):
        self.__content = None

        if pfx is not None:
            self.__content = base64.b64decode(pfx)

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    @property
    def content_base64(self):
        return base64.b64decode(self.__content)

    @content_base64.setter
    def content_base64(self, value):
        self.__content = base64.b64encode(value)

    def write_to_file(self, path):
        with open(path, 'wb') as f:
            f.write(self.__content)


__all__ = ['Pkcs12Certificate']
