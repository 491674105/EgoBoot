from sys import modules
from importlib import import_module
from traceback import format_exc

from threading import current_thread as get_current_thread
from logging import Logger

from flask import Flask
from flask import request, session, current_app, g
from flask import jsonify
from sqlalchemy.orm import sessionmaker

from ego import applicationContext
from ego.response.Result import Result
from ego.common.enum.network.ResultCode import ResultCode

from ego.filter.Filter import Filter
from ego.interceptor.Interceptor import Interceptor

from ego.exception.default.CustomException import CustomException
from ego.exception.api.APIException import APIException

app: Flask = applicationContext.app
log: Logger = applicationContext.log

actuator_package = "ego.controller.ActuatorController"
if actuator_package not in modules:
    getattr(import_module(actuator_package), "ActuatorController")


class Dispatcher(object):

    @staticmethod
    def __request_handle():
        if hasattr(applicationContext, "filters"):
            for order_id in applicationContext.filters:
                filter_class = applicationContext.filters[order_id]
                filter_: Filter = filter_class()
                filter_.app = applicationContext.app
                filter_.current_app = current_app
                filter_.request = request
                filter_.session = session
                filter_.g = g
                filter_.current_thread = get_current_thread()
                filter_.handle_access_log()
                filter_.do_filter()

        if hasattr(applicationContext, "interceptors"):
            for order_id in applicationContext.interceptors:
                interceptor_class = applicationContext.interceptors[order_id]
                interceptor_: Interceptor = interceptor_class()
                interceptor_.app = applicationContext.app
                interceptor_.current_app = current_app
                interceptor_.request = request
                interceptor_.session = session
                interceptor_.g = g
                if not interceptor_.pre_handle():
                    raise Exception()

                if not interceptor_.post_handle():
                    raise Exception()

                if not interceptor_.after_completion():
                    raise Exception()

    @staticmethod
    @app.before_request
    def before_request():
        current_thread = get_current_thread()
        applicationContext.uri_dict[current_thread.ident] = request.path
        host = Dispatcher.get_host()
        log.info(f"【{host}】 is accessing 【{request.path}】")
        Dispatcher.__request_handle()

    @staticmethod
    @app.after_request
    def after_request(response):
        log.info("HTTP/1.1 200")

        current_thread = get_current_thread()
        if current_thread.ident not in applicationContext.uri_dict:
            return response
        del applicationContext.uri_dict[current_thread.ident]

        return response

    @staticmethod
    @app.teardown_request
    def teardown_request(e):
        if e:
            log.exception(e)
            Dispatcher.handle_database_transaction(e)

            return jsonify(Result.failed(msg=e))

        return jsonify(Result.failed(msg="INTERNAL_SERVER_ERROR"))

    @staticmethod
    @app.errorhandler(400)
    def bad_request(e):
        """
            400处理
        """
        host = Dispatcher.get_host()
        log.error(f"【{host}】 is accessing 【{request.path}】")
        log.error(f"请求参数异常 ---> {request.get_data()}")

        return jsonify(Result(ResultCode.BAD_REQUEST.value, "BAD_REQUEST").body())

    @staticmethod
    @app.errorhandler(404)
    def not_found(e):
        """
            404处理
        """
        host = Dispatcher.get_host()
        log.error(f"【{host}】 is accessing 【{request.path}】")
        log.error(e)

        return jsonify(Result(ResultCode.NOT_FOUND.value, "NOT FOUND").body())

    @staticmethod
    @app.errorhandler(Exception)
    def framework_error(e):
        """
            异常处理
        """
        host = Dispatcher.get_host()
        log.error(f"【{host}】 is accessing 【{request.path}】")
        log.exception(e)

        Dispatcher.handle_database_transaction(e)

        msg = format_exc().split("\n")[-2]
        error = 500
        if isinstance(e, APIException):
            msg = e.msg
            error = e.error
        if isinstance(e, CustomException):
            msg = e.msg
            error = e.code

        return jsonify(
            Result(
                code=ResultCode.OK.value,
                msg=msg,
                data=Result.failed(code=error, msg=msg)
            ).body()
        )

    @staticmethod
    def handle_database_transaction(e):
        if not hasattr(applicationContext, "session"):
            return

        session_dict = getattr(applicationContext, "session")
        current_thread = get_current_thread()
        if current_thread.ident not in session_dict:
            return

        user_session = session_dict[current_thread.ident]
        if "sql_connect" not in user_session or not user_session["sql_connect"]:
            return

        connect = user_session["sql_connect"]
        session_maker = sessionmaker()
        session_maker.configure(bind=connect)
        session_inst = session_maker()
        if hasattr(e, "msg"):
            msg = e.msg
        else:
            msg = "操作异常！"
        log.error(msg)
        log.exception(e)
        session_inst.rollback()
        connect.close()

        # 清空会话缓存
        if current_thread.ident in applicationContext.session:
            del applicationContext.session[current_thread.ident]

    @staticmethod
    def get_host():
        if "X-Real-Ip" in request.headers and request.headers["X-Real-Ip"]:
            host = request.headers["X-Real-Ip"]
        else:
            host = request.remote_addr
        return host
