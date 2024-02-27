def typeof(variate):
    v_type = None
    if isinstance(variate, int):
        v_type = "int"
    elif isinstance(variate, str):
        v_type = "str"
    elif isinstance(variate, float):
        v_type = "float"
    elif isinstance(variate, list):
        v_type = "list"
    elif isinstance(variate, tuple):
        v_type = "tuple"
    elif isinstance(variate, dict):
        v_type = "dict"
    elif isinstance(variate, set):
        v_type = "set"
    return v_type
