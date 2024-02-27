import platform

from os import path, walk
from re import sub


def query_file_name_list(
        root_path: str, exclude_folder: list = None, exclude_name: list = None, exclude_type: list = None, **kwargs
):
    if not exclude_folder:
        exclude_folder = []
    if not exclude_name:
        exclude_name = []
    if not exclude_type:
        exclude_type = []

    file_name_list = []
    for root, dirs, files in walk(root_path):
        if path.split(root)[1] in exclude_folder:
            continue

        for file in files:
            file_attr = file.split(".")
            short_name = file_attr[0]
            suffix = file_attr[1]
            if short_name in exclude_name or suffix in exclude_type:
                continue

            if "regex_name" in kwargs and short_name.find(kwargs["regex_name"]) == -1:
                continue

            file_name_list.append(short_name)

    return file_name_list


def path_format(src_path):
    if platform.system().lower() != "windows":
        return sub(r"(\\+/*|/+|\\+)", "/", src_path)
    else:
        return sub(r"(\\+/*|/+|\\+)", "\\\\", src_path)


def get_sys_path_delimiter():
    if platform.system().lower() != "windows":
        return "/"
    else:
        return "\\"


def get_path(base_path="", up_level="../../.."):
    project_path = path.abspath(
        path.join(
            path.dirname(__file__),
            up_level,
        )
    )

    if platform.system().lower() != "windows":
        path_separator = "/"
    else:
        path_separator = "\\"
    if base_path and base_path != "":
        return f"{project_path}{path_separator}{base_path}{path_separator}"
    else:
        return f"{project_path}{path_separator}"


def package_format(src_path):
    project_path = get_path()
    relative_path = src_path.replace(project_path, "")
    relative_path = relative_path.replace("\\", ".")
    relative_path = relative_path.replace("/", ".")
    return relative_path
