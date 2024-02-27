from requests import request
from io import StringIO

from ego.common.enum.network.HttpMethod import HttpMethod
from ego.common.enum.network.ResultCode import ResultCode
from ego.network.http.Client import Client
from ego.network.http.default.HttpResponse import HttpResponse

from ego.exception.type.NullPointException import NullPointException


class HttpClient(Client):

    def create_url(self, uri, params=None):
        if not self.host or self.host == "":
            raise NullPointException("unknown host.")

        if self.host[-1] == "/":
            self.host = self.host[0:-2]

        if self.port <= 0:
            port = ""
        else:
            port = f":{self.port}"

        if uri[0] == "/":
            real_uri = uri[1:]
        else:
            real_uri = uri

        if "http" in self.host:
            return self.add_param_to_url(f"{self.host}{port}/{real_uri}", params)

        if self.use_ssl:
            protocol = "https://"
        else:
            protocol = "http://"

        return self.add_param_to_url(f"{protocol}{self.host}{port}/{real_uri}", params)

    @staticmethod
    def add_param_to_url(url, params=None):
        if not params:
            return url

        params_str = StringIO("")
        params_str.write(url)
        params_str.write("?")

        index = 0
        for param in params:
            if index > 0:
                params_str.write("&")
            params_str.write(param)
            params_str.write("=")
            params_str.write(str(params[param]))

            index += 1

        return params_str.getvalue()

    def __set_default_headers(self, method):
        if method == HttpMethod.POST.value:
            self.headers = {
                "Content-Type": "application/json"
            }
        else:
            self.headers = {
                "Content-Type": "application/text"
            }

    def open_original_request(self, method, url, params=None, headers=None, body=None, *args, **kwargs):
        if headers:
            self.headers.update(headers)

        response: HttpResponse = HttpResponse()
        try:
            res = request(
                method,
                url=url,
                params=params,
                headers=self.headers,
                data=body,
                *args,
                **kwargs
            )

            response.original = res

        except Exception as e:
            print(e)
            response.code = ResultCode.INTERNAL_SERVER_ERROR.value
            response.data = e

        return response

    def open_request(self, method, uri, params=None, headers=None, body=None, *args, **kwargs):
        url = self.create_url(uri)
        if headers:
            self.headers.update(headers)

        response: HttpResponse = HttpResponse()
        try:
            res = request(
                method,
                url=url,
                params=params,
                headers=self.headers,
                data=body,
                *args,
                **kwargs
            )

            response.original = res

        except Exception as e:
            print(e)
            response.code = ResultCode.INTERNAL_SERVER_ERROR.value
            response.data = e

        return response

    def get(self, uri, params=None, headers=None, *args, **kwargs):
        return self.open_request(HttpMethod.GET.value, uri, params=params, headers=headers, *args, **kwargs)

    def post(self, uri, params=None, headers=None, body=None, *args, **kwargs):
        return self.open_request(HttpMethod.POST.value, uri, params=params, headers=headers, body=body, *args, **kwargs)

    def put(self, uri, headers=None, body=None, *args, **kwargs):
        return self.open_request(HttpMethod.PUT.value, uri, headers=headers, body=body, *args, **kwargs)

    def delete(self, uri, headers=None, *args, **kwargs):
        return self.open_request(HttpMethod.DELETE.value, uri, headers=headers, *args, **kwargs)
