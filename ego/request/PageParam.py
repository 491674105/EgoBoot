from ego.request.BaseParam import BaseParam

from ego.common.enum.network.ResultCode import ResultCode

from ego.exception.api.APIException import APIException


class PageParam(BaseParam):
    __DEFAULT_PAGE_NO = 1
    __DEFAULT_PAGE_SIZE = 20

    def __init__(self, page_no=None, page_size=None, body=None):
        self.__body = None
        self.__pageable = True
        self.__page_no = None
        self.__page_size = None
        super().__init__()

        self.mapping_body(body)

        if page_no is None and self.__page_no is None:
            self.__page_no = self.__DEFAULT_PAGE_NO
        else:
            try:
                self.__page_no = int(self.__page_no)
                if self.__page_no <= 0:
                    raise APIException(code=ResultCode.BAD_REQUEST.value, msg="页码不可小于1")
            except ValueError:
                self.__page_no = self.__DEFAULT_PAGE_NO

        if page_size is None and self.__page_size is None:
            self.__page_size = self.__DEFAULT_PAGE_SIZE
        else:
            try:
                self.__page_size = int(self.__page_size)
                if self.__page_size <= 0:
                    raise APIException(code=ResultCode.BAD_REQUEST.value, msg="页行数不可小于1")
            except ValueError:
                self.__page_size = self.__DEFAULT_PAGE_SIZE

        self.__start = (self.__page_no - 1) * self.__page_size

    @property
    def pageable(self):
        return self.__pageable

    @property
    def page_no(self):
        return self.__page_no

    @page_no.setter
    def page_no(self, page_no: int):
        if page_no < 0:
            self.__page_no = self.__DEFAULT_PAGE_NO
            return

        self.__page_no = page_no

    @property
    def page_size(self):
        return self.__page_size

    @page_size.setter
    def page_size(self, page_size: int):
        if page_size < 0:
            self.__page_size = self.__DEFAULT_PAGE_SIZE
            return

        self.__page_size = page_size

    @property
    def body(self):
        return self.__body

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, start_):
        self.__start = start_

    def mapping_body(self, body=None):
        if not body:
            return

        self.__body = body
        for key, value in body.items():
            if key == "page_no":
                self.__page_no = int(value)
                continue
            if key == "page_size":
                self.__page_size = int(value)
                continue

            if key == "pageable":
                self.__pageable = bool(value)
                continue

            if value is not None:
                setattr(self, key, value)
