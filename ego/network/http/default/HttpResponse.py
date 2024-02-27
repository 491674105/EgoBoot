from typing import Union
from json import loads

from requests import Response as OriginalResponse

from ego.network.http.Response import Response


class HttpResponse(Response):

    def __init__(self):
        super().__init__(0)

        self.__response: Union[OriginalResponse, None] = None

    @property
    def original(self) -> OriginalResponse:
        return self.__response

    @original.setter
    def original(self, original: OriginalResponse):
        self.__response = original

        self.code = original.status_code
        self.headers = original.headers
        self.encoding = original.encoding
        self.data = original.content

    def get_json(self, *args, **kwargs):
        return loads(self.data.decode(self.encoding))
