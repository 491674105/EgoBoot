from ego.interceptor.Interceptor import Interceptor


class RequestInterceptor(Interceptor):
    order_id = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
