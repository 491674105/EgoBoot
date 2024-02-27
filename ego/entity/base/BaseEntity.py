from sqlalchemy.ext.declarative import declarative_base

from ego import applicationContext

Base = declarative_base()


class BaseEntity:
    def __init__(self, s_obj=None):
        self.data_set = None
        self.obj = None
        self.keys = None
        if s_obj is not None:
            self.data_set = s_obj
            self.__use_default_entity = False
        else:
            self.__use_default_entity = True

    def to_dict_trans(self, trans_dict, include_none=False):
        result = {}
        for key in self.keys:
            value = getattr(self.obj, key)
            if value is None and not include_none:
                continue

            if key not in trans_dict:
                result[key] = value
                continue

            enum_ = trans_dict[key]
            if enum_.description.value and value is not None:
                result[key + "_code"] = value
                result[key] = enum_.description.value[value]
            else:
                result[key] = str(enum_(value).name)

        return result

    def to_dict(self, include_none=False, trans_dict=None):
        """
            将查询结果转换为dict，以适应前后端的json编码规则，适用于单条记录传输
            trans_dict: 需要进行翻译的字段{字段名: 解释枚举}
        """

        self.get_attributes()

        try:
            # 包含枚举内容时，需进行转换
            if trans_dict:
                return self.to_dict_trans(trans_dict=trans_dict, include_none=include_none)

            result = {}
            for key in self.keys:
                value = getattr(self.obj, key)
                if value is None and not include_none:
                    continue
                result[key] = getattr(self.obj, key)
            return result
        except Exception as e:
            if hasattr(applicationContext, "log"):
                log = applicationContext.log
                log.error("Unable to convert.")
                log.error(self.keys)
                log.error(self.obj)
                log.exception(e)
            return {}

    def get_attributes(self):
        if self.__use_default_entity or hasattr(self, "__mapper__"):
            self.obj = self
            self.keys = self.__mapper__.c.keys()
        else:
            try:
                self.obj = self.data_set
                self.keys = getattr(self.data_set, "_fields")
            except AttributeError:
                self.obj = self.data_set
                self.keys = []
                for attr_name in dir(self.obj):
                    if attr_name.find("_") == 0:
                        continue
                    self.keys.append(attr_name)
