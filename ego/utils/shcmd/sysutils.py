from os import getpid
from sys import stdout

from psutil import process_iter

from ego.common.constant.config import Base


def get_pid(p_name):
    """
        获取指定服务的PID
    """
    if not p_name:
        return -1

    process_list = process_iter()
    for process in process_list:
        if process.pid == getpid():
            return process

    return -1


def print_logo():
    logo_lines = [
        "                                  ",
        "                                  ",
        "      ,---,.                      ",
        "    ,'  .' |                      ",
        "  ,---.'   |              ,---.   ",
        "  |   |   .'  ,----._,.  '   ,'\\  ",
        "  :   :  |-, /   /  ' / /   /   | ",
        "  :   |  ;/||   :     |.   ; ,. : ",
        "  |   :   .'|   | .\\  .'   | |: : ",
        "  |   |  |-,.   ; ';  |'   | .; : ",
        "  '   :  ;/|'   .   . ||   :    | ",
        "  |   |    \\ `---`-'| | \\   \\  /  ",
        "  |   :   .' .'__/\\_: |  `----'   ",
        "  |   | ,'   |   :    :           ",
        "  `----'      \\   \\  /            ",
        "               `--`-'             ",
        f"{Base.VERSION_}",
        "                                  ",
        "                                  "
    ]
    for line in logo_lines:
        stdout.write(line)
        stdout.write('\n')
