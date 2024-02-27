from urllib.parse import unquote

from ego.filter.Filter import Filter
from ego.common.constant.config.Base import DEFAULT_ENCODING
from ego.entity.dto.auth.RedisUserDTO import RedisUserDTO


class RequestFilter(Filter):
    order_id = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def do_filter(self):
        """
            header数据过滤
            g.user_info：请求用户信息
            g.params：请求参数集
        """
        super().do_filter()
        user_info = RedisUserDTO()
        for key in dir(user_info):
            if key.find("__") == 0:
                continue

            if key in self.request.headers:
                value = unquote(self.request.headers[key], encoding=DEFAULT_ENCODING)
                setattr(
                    user_info,
                    key,
                    value
                )

        self.g.user_info = user_info
        return True

    def __del__(self):
        pass
