from __future__ import annotations
import os
import sys
from datetime import datetime

"""
PyCharm sets PythonPath to the Content Root folder, VSC does not by default, causing import failures

Hence, add this to the VSCode launch config:
"env": {"PYTHONPATH": "${workspaceFolder}:${env:PYTHONPATH}"}

ref: https://stackoverflow.com/questions/53653083/how-to-correctly-set-pythonpath-for-visual-studio-code

Or, use the function below.
"""


def is_found(node: str, target: str, wild_card: bool) -> bool:
    if wild_card:
        found = node.startswith(target)
    else:
        found = node == target
    return found


def add_python_path(project_dir: str, my_file: str) -> (str, str):
    """
    @param project_dir: enclosing path node, case insensitive, with optional "*" for starts-with (e.g., LogicBank, LogicBank*)
    @param my_file: callers __file__ variable
    @result (path_was_fixed, path)

    """
    target_last_node = project_dir.lower()
    wild_card = False
    if target_last_node.endswith('*'):
        wild_card = True
        target_last_node = target_last_node[0: len(target_last_node) - 1]
    current_path = os.path.abspath(os.path.dirname(my_file))
    each_last_node = ""
    while not is_found(node=each_last_node, target=target_last_node, wild_card=wild_card):
        each_last_node = os.path.basename(os.path.normpath(current_path))
        each_last_node = each_last_node.lower()
        found = is_found(node=each_last_node, target=target_last_node, wild_card=wild_card)
        if not found:
            current_path = os.path.dirname(current_path)
            if current_path == "/":
                raise Exception("project_dir not found: " + target_last_node)

    sys_path = ""
    required_path_present = False
    for each_last_node in sys.path:
        sys_path += each_last_node + "\n"
        if each_last_node == current_path:
            required_path_present = True
    if not required_path_present:
        result_was_fixed = "Fixing path (so can run from terminal)"
        sys.path.append(current_path)
    else:
        pass
        result_was_fixed = "NOT Fixing path (default PyCharm, set in VSC Launch Config)"
    run_env_info = \
        "**************** add_python_path BEGIN\t\t" +\
        "calling file: " + my_file + "\n\n" +\
        get_run_environment_info() +\
        "fix path: " + result_was_fixed + "\n\n"\
        "**************** add_python_path END"
    return result_was_fixed, run_env_info


def get_sys_path():
    """
    :return: readable, multi-line output of Python Path
    """
    sys_path = ""
    for each_node in sys.path:
        sys_path += each_node + "\n"
    return sys_path


def get_run_environment_info() -> str:
    """
    @return: readable, multi-line output of Python environment
    """
    cwd = os.getcwd()   # eg, /Users/val/dev/logicbank/nw/tests
    run_environment_info = "Run Environment info...\n\n"
    run_environment_info += "Current Working Directory: " + cwd + "\n\n"
    run_environment_info += "sys.path: (Python imports)\n" + get_sys_path() + "\n"
    run_environment_info += "From: " + sys.argv[0] + "\n\n"
    run_environment_info += "Using Python: " + sys.version + "\n\n"
    run_environment_info += "At: " + str(datetime.now()) + "\n\n"
    return run_environment_info

if __name__ == "__main__":
    # execute only if run as a script
    print("\nRunning with __file__: " + __file__ + ", sys_path:\n" + get_sys_path())

    result_was_fixed, run_env_info = add_python_path(project_dir="LogicBankUtils", my_file=__file__)
    print("\n\nCompleted 'LogicBankUtils': path fixed? " + result_was_fixed + ", result is\n" + get_sys_path())

    result_was_fixed, run_env_info = add_python_path(project_dir="LogicBankUtil*", my_file=__file__)
    print("\n\nCompleted 'LogicBankUtil*': path fixed? " + result_was_fixed + ", result is\n" + get_sys_path())

    result_was_fixed, run_env_info = add_python_path(project_dir="LogicBankUtilx", my_file=__file__)
    print("\n\nCompleted 'LogicBankUtilx': path fixed? " + result_was_fixed + ", result is\n" +  get_sys_path())
