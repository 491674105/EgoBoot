from flask import request

from functools import wraps

from ego import applicationContext
from ego.dispatch.MappingDispatcher import Mapping
from ego.common.enum.network.HttpMethod import HttpMethod
from ego.common.enum.system.OpType import OpType


class RequestMapping(Mapping):
    def __init__(self, path=None, methods=None, param_mappings=None, record_log=False, record_log_type=OpType.NORMAL, *args):
        """
            record_log: 启用接口访问操作记录，必须保证日志表在对应数据库中存在（默认：False）
                表结构创建脚本：ego/resources/database/init.sql -> operate_log & operate_log_detail
            record_log_type: 接口操作类型
        """
        super().__init__(
            path=path, methods=methods, param_mappings=param_mappings,
            record_log=record_log, record_log_type=record_log_type,
            *args
        )

    def __call__(self, func):
        package_name = func.__module__
        endpoint = f"{package_name}.{func.__name__}"

        api_record = {
            "rule": self.get_api_path(),
            "endpoint": endpoint,
            "methods": self.get_api_methods()
        }

        if not hasattr(applicationContext, "api_records"):
            setattr(applicationContext, "api_records", {})

        if package_name in getattr(applicationContext, "api_records"):
            applicationContext.api_records[package_name].append(api_record)
        else:
            applicationContext.api_records[package_name] = [api_record]

        endpoint_info = endpoint.rsplit(".", 1)
        real_endpoint = f"{endpoint_info[0].replace('.', '-')}.{endpoint_info[1]}"
        if self.record_log and real_endpoint not in applicationContext.record_log_endpoints:
            applicationContext.record_log_endpoints[real_endpoint] = self.record_log_type

        @wraps(func)
        def wrapper(*args, **kwargs):
            self.set_args(args)
            self.set_kwargs(kwargs)

            if func.__code__.co_argcount <= 1 or request.method == HttpMethod.GET.value:
                self.ncalls += 1
                return func(*self.get_args(), **self.get_kwargs())

            func_code = getattr(func, "__code__")
            arg_count = getattr(func_code, "co_argcount")
            arg_names = getattr(func_code, "co_varnames")
            self.set_multi_params(arg_count, arg_names)
            self.ncalls += 1
            return func(*self.get_args(), **self.get_kwargs())

        return wrapper
