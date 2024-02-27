from re import sub
from flask import Blueprint, request, g
from flask.views import View

from ego import applicationContext

from ego.common.constant.config import Base

# app = applicationContext.app


class Controller:

    def __init__(self, path=None, sys_root=True, *args):
        """
            path: 控制层路径
            sys_root: 是否调用系统根路由，由项目配置提供（ROOT_PATH常量）
        """
        self.ncalls = 0

        if path:
            self.__controller_path = f"/{path}"
        elif len(args) > 0:
            self.__controller_path = f"/{args[0]}"
        else:
            self.__controller_path = "/"

        root_path = applicationContext.base_config[
            getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)
        ]["root_path"]
        if sys_root and root_path:
            self.__controller_path = f"{root_path}/{self.__controller_path}"

        self.__controller_path = sub(r"/+", "/", self.__controller_path)
        self.__route = None

    def __call__(self, clazz):
        def dispatch_request(this, *args, **kwargs):
            if args:
                setattr(g, "args", args)

            if kwargs:
                setattr(g, "kwargs", kwargs)

            return getattr(this, getattr(applicationContext, "api_mappings")[request.url_rule.rule])()

        attrs = {
            "dispatch_request": dispatch_request
        }
        for key in clazz.__dict__:
            if key.find("__") == 0 or key.find(f"_{clazz.__name__}") > 0:
                continue
            attrs[key] = clazz.__dict__[key]

        m_clazz = type(clazz.__name__, (View,), attrs)

        self.__route = Blueprint(
            name=clazz.__module__.replace(".", "-"),
            import_name=clazz.__module__,
            url_prefix=self.__controller_path
        )

        api_records = getattr(applicationContext, "api_records")
        api_mappings = {}
        for api_record in api_records[clazz.__module__]:
            api_url = api_record["rule"]
            endpoint = api_record["endpoint"]
            view_func = endpoint.split(".")[-1]
            self.__route.add_url_rule(
                rule=api_url,
                endpoint=view_func,
                view_func=getattr(m_clazz, "as_view")(view_func),
                methods=api_record["methods"]
            )
            api_mappings[f"{self.__controller_path}{api_url}"] = view_func

        if not hasattr(applicationContext, "api_mappings"):
            setattr(applicationContext, "api_mappings", api_mappings)
        else:
            getattr(applicationContext, "api_mappings").update(api_mappings)
        # app.register_blueprint(blueprint=self.__route)
        applicationContext.bp_set = self.__route
