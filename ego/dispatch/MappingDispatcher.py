from functools import wraps
from json import loads

from re import sub
from flask import request, g

from ego import applicationContext
from ego.common.enum.network.HttpMethod import HttpMethod
from ego.common.enum.system.OpType import OpType


class Mapping:
    def __init__(self, path=None, methods=None, param_mappings=None, record_log=False, record_log_type=OpType.NORMAL, *args):
        """
            path: API路径
            methods: API请求方式
            params: 请求参数与API入口函数入参对应关系
                key: 函数入参名
                value: Http Body中的参数名
        """
        self.ncalls = 0
        if path:
            self.__api_path = f"/{path}"
        elif len(args) > 0:
            self.__api_path = f"/{args[0]}"
        else:
            self.__api_path = "/"

        self.__api_path = sub(r"/+", "/", self.__api_path)

        self.__api_methods = []
        if not methods:
            self.__api_methods.append(HttpMethod.GET.value)
        elif isinstance(methods, list):
            self.__api_methods = [method.value for method in methods]
        else:
            self.__api_methods.append(methods.value)

        self.__api_param_mappings = {}
        if param_mappings:
            self.__api_param_mappings = param_mappings

        self.__record_log = record_log
        self.__record_log_type = record_log_type

        self.__args = ()
        self.__kwargs = {}

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    @property
    def record_log(self):
        return self.__record_log

    @record_log.setter
    def record_log(self, record_log_):
        self.__record_log = record_log_

    @property
    def record_log_type(self):
        return self.__record_log_type

    @record_log_type.setter
    def record_log_type(self, record_log_type_):
        self.__record_log_type = record_log_type_

    @staticmethod
    def __get_request_params():
        kwargs = {}
        if "application/json" in request.content_type:
            kwargs["request_body"] = request.get_json()

        if "application/text" in request.content_type:
            params = request.get_data()
            try:
                kwargs["request_body"] = loads(params)
            except Exception as e:
                applicationContext.log.error(f"Decoding failure. {params}")
                raise e

        if request.args:
            for r_key in request.args:
                kwargs[r_key] = request.args[r_key]

        if hasattr(g, "kwargs"):
            kwargs.update(g.kwargs)

        if request.files:
            kwargs["multi_files"] = request.files

        if request.data:
            kwargs["input_stream"] = request.data

        return kwargs

    def __set_multi_params(self, arg_count, arg_names):
        kwargs = self.__get_request_params()
        applicationContext.log.debug(f"self.__api_param_mappings -> {self.__api_param_mappings}")
        applicationContext.log.debug(f"kwargs -> {kwargs}")

        if not self.__api_param_mappings:
            for index in range(1, arg_count):
                arg_name = arg_names[index]
                if arg_name in kwargs:
                    self.__args = self.__args + (kwargs[arg_name],)
            return

        for index in range(1, arg_count):
            arg_name = arg_names[index]
            arg = kwargs[self.__api_param_mappings[arg_name]]
            self.__args = self.__args + (arg,)

    def get_api_path(self):
        return self.__api_path

    def get_api_methods(self):
        return self.__api_methods

    def get_api_param_mappings(self):
        return self.__api_param_mappings

    def set_args(self, args):
        self.__args = args

    def get_args(self):
        return self.__args

    def set_multi_params(self, arg_count, arg_names):
        self.__set_multi_params(arg_count, arg_names)

    def set_kwargs(self, kwargs):
        self.__kwargs = kwargs

    def get_kwargs(self):
        return self.__kwargs
