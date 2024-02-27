from logging import Logger
from threading import current_thread as get_current_thread

from sqlalchemy.engine.base import Engine
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import dialects
from sqlalchemy.orm import sessionmaker

from ego import applicationContext
from ego.entity.base.BaseEntity import BaseEntity

if hasattr(applicationContext, "log"):
    log = getattr(applicationContext, "log")
else:
    log = Logger(name="BaseMapperLogger")
    log.setLevel("INFO")


class BaseMapper:
    def __init__(self, engine):
        self.engine: Engine = engine
        self.transaction = None

        global log
        if hasattr(applicationContext, "log"):
            log = getattr(applicationContext, "log")

        self.result_set = None

    def __is_base_entity(self):
        if isinstance(self.result_set, BaseEntity):
            return True
        return False

    def __handle_set(self, trans_dict, include_none):
        data_list = []
        for res in self.result_set:
            data_list.append(res.to_dict(include_none=include_none, trans_dict=trans_dict))
        return data_list

    def __handle_set_not_base_entity(self, trans_dict, include_none):
        data_list = []
        for res in self.result_set:
            data_list.append(BaseEntity(res).to_dict(include_none=include_none, trans_dict=trans_dict))
        return data_list

    def to_list(self, result_set, trans_dict=None, include_none=False):
        """
            将查询结果转换为list，适用于多条记录传输
        """
        if not result_set or len(result_set) == 0:
            return []
        try:
            self.result_set = result_set.copy()
        except AttributeError:
            self.result_set = result_set
        if self.__is_base_entity():
            return self.__handle_set(trans_dict=trans_dict, include_none=include_none)
        else:
            return self.__handle_set_not_base_entity(trans_dict=trans_dict, include_none=include_none)

    def select(self, select_sql, count_flag=True, group_by=None, order_by=None, offset=None, limit=None):
        """
            通用查询（主要用于分页列表查询）
            select_sql: 查询SQL结构
            count_flag: 统计标识，为真时，会在查询之前统计满足当前查询逻辑（不包含排序、分页）的总行数
            group_by: 分组聚合条件
            order_by: 排序条件
            offset: 查询起始位
            limit: 查询行数
            return:
                0: rowcout
                1: result_set
        """
        if group_by:
            if not isinstance(group_by, tuple):
                select_sql = select_sql.group_by(group_by)
            else:
                for param in group_by:
                    select_sql = select_sql.group_by(param)

        count_set = None
        if count_flag:
            with self.engine.begin() as connect:
                count_set = connect.execute(
                    select(func.count("*").label("rowcount")).select_from(select_sql.subquery()).compile(
                        dialect=getattr(dialects, self.engine.dialect.name).dialect()
                    )
                ).fetchone()

        if order_by is not None:
            if not isinstance(order_by, tuple):
                select_sql = select_sql.order_by(order_by)
            else:
                for param in order_by:
                    select_sql = select_sql.order_by(param)

        if offset is not None and limit is not None:
            select_sql = select_sql.offset(offset).limit(limit)

        with self.engine.begin() as connect:
            response_set = connect.execute(
                select_sql.compile(dialect=getattr(dialects, self.engine.dialect.name).dialect())
            ).all()

        return count_set.rowcount, response_set

    def transactional(self, sql_struct, get_insert_pk=False, get_rowcount=False, **kwargs):
        current_thread = get_current_thread()
        if not hasattr(applicationContext, "session"):
            setattr(applicationContext, "session", {current_thread.ident: {}})

        session_dict = getattr(applicationContext, "session")
        if current_thread.ident not in session_dict:
            applicationContext.session[current_thread.ident] = {}

        user_session = session_dict[current_thread.ident]
        if "sql_connect" not in user_session or not user_session["sql_connect"]:
            connect = self.engine.connect()

            applicationContext.session[current_thread.ident]["sql_connect"] = connect
        else:
            connect = user_session["sql_connect"]
        session_maker = sessionmaker(**kwargs)
        session_maker.configure(bind=connect)
        session = session_maker()

        cache_value = None
        session.begin_nested()
        cache_response = session.execute(sql_struct)
        if get_insert_pk and hasattr(cache_response, "inserted_primary_key"):
            cache_value = getattr(cache_response, "inserted_primary_key")[0]
        if get_rowcount and hasattr(cache_response, "rowcount"):
            cache_value = getattr(cache_response, "rowcount")

        session.commit()

        return cache_value
