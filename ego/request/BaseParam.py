

class BaseParam:

    def __init__(self, body=None):
        self.__body = None
        self.mapping_body(body)

    @property
    def body(self):
        return self.__body

    def mapping_body(self, body=None):
        if not body:
            return

        self.__body = body
        for key, value in body.items():
            if value is not None:
                setattr(self, key, value)
