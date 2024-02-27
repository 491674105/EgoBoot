from time import sleep

from uuid import uuid5
from uuid import NAMESPACE_DNS

from ego.utils.time.Time import get_time_of_ms


def get_for_unique_uuid(name=None):
    sleep(0.01)
    if not name:
        name = f"default{get_time_of_ms()}"
    else:
        name = f"{name}{get_time_of_ms()}"
    return uuid5(NAMESPACE_DNS, name)


if __name__ == "__main__":
    end = 11
    for step in range(1, end):
        uuid_str = get_for_unique_uuid(name="default")
        # print(f"{step} --> {uuid_str}")
        print(uuid_str)
