from snippet.snippet import StringCodec


class Wordcount(StringCodec):
    """ Return the number of words. """

    def __init__(self):
        super().__init__(author="bytebutcher", dependencies=[])

    def run(self, content):
        return str(len(content.split()))