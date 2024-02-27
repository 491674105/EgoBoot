# Unix/Linux环境下有效
try:
    from fcntl import flock
    from fcntl import LOCK_EX, LOCK_NB, LOCK_UN

    lock_module_valid = True
except ModuleNotFoundError:
    lock_module_valid = False

from ego.exception.type.NullPointException import NullPointException


def lock(file):
    if lock_module_valid:
        try:
            flock(file, LOCK_EX | LOCK_NB)
            return True
        except OSError:
            return False

    return False


def lock_file_path(file_path):
    if not file_path:
        raise NullPointException("file_path can not null!")

    lock_file = open(f"{file_path}", "wb+")
    try:
        # 获取锁
        return lock(lock_file)
    except OSError:
        # 无法获取锁，认为有其他进程完成持锁
        return False


def un_lock(file):
    try:
        if lock_module_valid:
            flock(file, LOCK_UN)
            file.close()
            return True

        file.close()
        return False
    except OSError:
        return False
