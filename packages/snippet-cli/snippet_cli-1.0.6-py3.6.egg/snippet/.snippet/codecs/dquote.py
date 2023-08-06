from snippet.snippet import StringCodec


class Dquote(StringCodec):
    """ Surrounds a string with double quotes. """

    def __init__(self):
        super().__init__(author="bytebutcher", dependencies=[])

    def run(self, input):
        return '"{}"'.format(input)