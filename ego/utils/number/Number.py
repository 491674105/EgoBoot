from hashlib import md5


def calc_number_digits(num):
    """
        计算整数位数（通用方法）
    """
    if num == 0:
        return 1

    digits = 0
    while num > 1 or num < -1:
        num = num / 10
        digits += 1
    return digits


meta_integer_list = [
    9, 99, 999,
    9999, 99999, 999999,
    9999999, 99999999, 999999999,
    9999999999
]


def calc_integer_digits(num):
    """
        快速判断整数位数（限10亿量级内数值判断）
    """
    index = 0
    while index < len(meta_integer_list):
        if num <= meta_integer_list[index]:
            return index + 1

    return -1


def string_to_random_number(src, out_len=11):
    """
        将输入的字符串转换为指定长度的hash数值
    """
    hash_object = md5(src.encode())
    hex_hash = hash_object.hexdigest()

    result = int(hex_hash, 16)

    return result % (10 ** out_len)
