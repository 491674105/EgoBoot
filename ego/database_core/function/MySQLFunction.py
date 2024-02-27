from sqlalchemy.sql import sqltypes
from sqlalchemy.sql.functions import GenericFunction


class group_concat(GenericFunction):
    type = sqltypes.String()
    inherit_cache = True
