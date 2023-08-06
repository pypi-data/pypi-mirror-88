from snippet.snippet import ListCodec


class Join(ListCodec):
    """ Takes a list of items and joins them with the specified separator. """

    def __init__(self):
        super().__init__(author="bytebutcher", dependencies=[])

    def run(self, input, separator):
        return [separator.join(input)]