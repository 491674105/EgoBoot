class NullPointException(Exception):
    def __init__(self, msg):
        super(NullPointException, self).__init__(msg)
