import subprocess as sp
import shlex


def execute(command=None, stdin=None, stdout=None, stderr=None, shell=False, timeout=None):
    if not shell:
        process = sp.Popen(command, stdin=stdin, stdout=stdout, stderr=stderr)
    else:
        process = sp.check_output(command, shell=shell)

    return process


def execute_bash(command=None):
    """
        直接调用系统shell执行当前命令（危险操作，不推荐）
    """
    return execute(shlex.split(command), shell=True)


def execute_commands(command):
    result = None

    commands = command.split("|")

    index = 0
    for command in commands:
        if index > 0:
            result = execute(
                shlex.split(command), stdin=result.stdout, stdout=sp.PIPE, stderr=sp.STDOUT
            )
        else:
            result = execute(shlex.split(command), stdout=sp.PIPE, stderr=sp.STDOUT)
        index += 1

    return result
