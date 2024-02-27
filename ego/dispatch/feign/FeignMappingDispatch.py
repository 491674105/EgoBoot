from logging import Logger
from threading import current_thread as get_current_thread
from functools import wraps

from socket import timeout
from json import loads, dumps
from http import HTTPStatus
from urllib.request import Request, urlopen, ProxyHandler, HTTPSHandler, build_opener
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError

from ego import routeContainer
from ego.dispatch.MappingDispatcher import Mapping
from ego.common.enum.network.HttpMethod import HttpMethod
from ego.exception.feign.FeignException import FeignException

try:
    import ssl
except ImportError:
    ssl = None


class FeignMapping(Mapping):
    __get_headers = {
        "Content-Type": "application/text"
    }
    __post_headers = {
        "Content-Type": "application/json"
    }
    __response = None

    __server_info = None

    def __init__(self, service_name, uri, headers=None, params=None, data=None, **kwargs):
        """
            service_name: feign_server名称
            uri: 接口路径
            header: 静态header属性
            params: 静态url后缀（可以是get参数）
            data: 静态request_body（用于POST请求）
            method: 请求方式（GET、POST）
            timeout: 请求超时
            proxies: 请求代理
        """

        self.ncalls = 0
        self.log: Logger = routeContainer.log

        self.service_name = service_name
        self.uri_model = uri
        self.hosts = {}
        self.headers = {}
        if headers:
            self.headers = headers
        self.params = {}
        if params:
            self.params = params
        self.data = {}
        if data:
            self.data = data
        self.kwargs_dict = {}
        self.method = HttpMethod.GET
        self.timeout = 5
        self.proxies = {}
        if kwargs:
            if "method" in kwargs:
                self.method = kwargs["method"]
            if "timeout" in kwargs:
                self.timeout = kwargs["timeout"]
            if "proxies" in kwargs:
                self.proxies = kwargs["proxies"]

    def __call__(self, func):
        self.func = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            if "service_name" in kwargs and kwargs["service_name"] not in (None, ""):
                self.service_name = kwargs["service_name"]

            current_thread = get_current_thread()
            try:
                if "service_instances" in kwargs and kwargs["service_instances"]:
                    self.hosts[current_thread.ident] = kwargs["service_instances"]
                else:
                    self.hosts[current_thread.ident] = routeContainer.service_instances[self.service_name].copy()
            except KeyError:
                self.log.error(f"服务[{self.service_name}]订阅信息丢失！")
                return

            if kwargs:
                self.kwargs_dict = kwargs

            self.uri = self.uri_model
            if '{' in self.uri:
                self.__handler_dynamic_uri()

            if "api_path" in kwargs:
                api_path = kwargs["api_path"]
                if self.uri[-1] == "/" or api_path[0] == "/":
                    self.uri = f"{self.uri}{api_path}"
                else:
                    self.uri = f"{self.uri}/{api_path}"

            if "header" in kwargs:
                self.headers.update(kwargs["header"])

            if "params" in kwargs:
                self.params = kwargs["params"]

            if "data" in kwargs:
                self.data = kwargs["data"]

            self.__feign_request()
            kwargs["response"] = self.__response

            self.ncalls += 1
            return func(*args, **kwargs)

        return wrapper

    def __handler_dynamic_uri(self):
        if self.uri is None or self.uri == "":
            return

        uri_cache = self.uri
        index = 0
        uri_len = len(self.uri)
        start = -1
        while index < uri_len:
            ch = self.uri[index]
            if ch == "{":
                index += 1
                start = index
                continue
            if ch == "}":
                end = index
                index += 1
                this_param = self.uri[start:end]
                if this_param not in self.kwargs_dict:
                    raise KeyError(f"【{this_param}】is not found!")
                uri_cache = uri_cache.replace(f"{{{this_param}}}", self.kwargs_dict[this_param])
                continue
            index += 1
        self.uri = uri_cache

    def __get_common_headers(self):
        if self.method and self.method == HttpMethod.POST:
            return self.__post_headers
        else:
            return self.__get_headers

    def __get_service(self):
        current_thread = get_current_thread()
        if current_thread.ident not in self.hosts:
            self.log.error(f"服务[{self.service_name}]主机信息异常！")
            return

        service_instances = self.hosts[current_thread.ident]
        unique_key = None
        for uk in service_instances:
            unique_key = uk
            host = service_instances[uk]
        del self.hosts[current_thread.ident][unique_key]
        return host

    def __feign_request(self):
        self.uri = "?".join(
            [self.uri, urlencode(self.params)]
        ) if self.params else self.uri
        all_headers = self.__get_common_headers()
        if hasattr(self, "headers"):
            all_headers.update(self.headers)
        request_info = "[feign_request]"
        request_info = f"{request_info} uri:{self.uri}"
        request_info = f"{request_info}, headers:{all_headers}"
        request_info = f"{request_info}, params:{self.params}"
        request_info = f"{request_info}, data:{self.data}"
        self.log.debug(request_info)

        tries = 0
        while True:
            self.__server_info = self.__get_service()

            if not self.__server_info:
                self.log.error("[do-sync-req] can not get one server.")
                raise FeignException("Server is not available.")

            server = ":".join(
                [self.__server_info["ip"], str(self.__server_info["port"])]
            )

            server_uri = server
            if not server_uri.startswith("http"):
                server_uri = "%s://%s" % ("http", server)

            req_body = None
            if self.data:
                if "Content-Type" in all_headers and all_headers["Content-Type"].find("json") != -1:
                    req_body = dumps(self.data).encode()
                else:
                    req_body = urlencode(self.data).encode()

            req = Request(
                url=server_uri + self.uri,
                data=req_body,
                headers=all_headers
            )
            req.get_method = lambda: self.method.value

            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            try:
                if self.proxies:
                    proxy_support = ProxyHandler(self.proxies)
                    https_support = HTTPSHandler(context=ctx)
                    opener = build_opener(proxy_support, https_support)
                    res = opener.open(req, timeout=self.timeout)
                else:
                    res = urlopen(req, timeout=self.timeout, context=ctx)
                if res.code != 200:
                    self.log.error("[do-sync-req] code:%s access server[%s] exception!" % (res.code, server))
                if "application/json" in res.headers["Content-Type"]:
                    if "charset" in res.headers["Content-Type"]:
                        self.__response = loads(res.read().decode(res.headers["Content-Type"].split("charset=")[1]))
                    else:
                        self.__response = loads(res.read().decode("UTF-8"))
                else:
                    self.__response = res
                break
            except HTTPError as e:
                if e.code in [
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    HTTPStatus.BAD_GATEWAY,
                    HTTPStatus.SERVICE_UNAVAILABLE
                ]:
                    self.log.warning(
                        "[do-sync-req] server:%s is not available for reason:%s" % (
                            server,
                            getattr(e, "msg")
                        )
                    )
                else:
                    self.log.exception(e)
            except timeout:
                self.log.warning("[do-sync-req] %s request timeout" % server)
            except URLError as e:
                self.log.warning(
                    "[do-sync-req] %s connection error:%s" % (server, e.reason)
                )

            tries += 1
            current_thread = get_current_thread()
            if tries >= len(self.hosts[current_thread.ident]):
                self.log.error(
                    "[do-sync-req] %s maybe down, no server is currently available" % server
                )
                break
            self.__server_info = self.__get_service()
            self.log.warning("[do-sync-req] %s maybe down, skip to next" % server)
