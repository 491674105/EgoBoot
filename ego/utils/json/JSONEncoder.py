from typing import Union, Any
from uuid import UUID
from datetime import datetime, date
from decimal import Decimal

from flask.json.provider import JSONProvider, DefaultJSONProvider


class JSONEncoder(DefaultJSONProvider):
    ensure_ascii = False

    def dumps(self, obj: Any, **kwargs: Any) -> str:
        return super(JSONEncoder, self).dumps(obj, **kwargs)

    def loads(self, s: Union[str, bytes], **kwargs: Any) -> Any:
        return super(JSONEncoder, self).loads(s, **kwargs)

    def default(self, obj):
        if isinstance(obj, datetime):
            # 格式化时间
            return obj.strftime("%Y-%m-%d %H:%M:%S") if obj is not None else None
        if isinstance(obj, date):
            # 格式化日期
            return obj.strftime("%Y-%m-%d") if obj is not None else None
        if isinstance(obj, Decimal):
            # 格式化高精度数字
            return str(obj)
        if isinstance(obj, UUID):
            # 格式化uuid
            return str(obj)
        if isinstance(obj, bytes):
            # 格式化字节数据
            return obj.decode("utf-8")
        # 其他需要处理的对象转换成可编码成json的对象
        return super(JSONEncoder, self).default(obj)
