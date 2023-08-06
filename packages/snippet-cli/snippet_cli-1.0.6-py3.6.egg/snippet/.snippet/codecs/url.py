from snippet.snippet import StringCodec


class Url(StringCodec):
    """ Encodes a string to an URL. """

    def __init__(self):
        super().__init__(author="bytebutcher", dependencies=["urllib"])

    def run(self, input):
        import urllib.parse
        return urllib.parse.quote(input.encode('utf-8', errors='surrogateescape'))