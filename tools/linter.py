#!/usr/bin/python3
"""Captures output of linting tools. Dependencies: pylint and pydocstlye."""

import os
import subprocess
import sys

def target_is_in_cwd(target):
    """Determine if the target file or dir is in PWD."""
    current_dir = os.getcwd()
    files_in_cwd = os.listdir(current_dir)
    for item in files_in_cwd:
        if item == target:
            return True
    return False

def find_target_in_project(project_root, target):
    """
    Walk through the project file structure and find target file.

    Return string name of the file or directory matching the target.
    Return empty string if target is not found in the project.
    """
    for root, dirs, files in os.walk(os.chdir(project_root), topdown=False):
        for name in files:
            if name == target:
                return os.path.abspath(os.path.join(root, name))
        for name in dirs:
            if name == target:
                return os.path.abspath(os.path.join(root, name))
    return ""

def get_project_root_directory():
    """Return the absolute path of the project's root directory."""
    current_directory = os.getcwd()
    cwd_parts = current_directory.split(os.sep)
    cwd_parts = cwd_parts[:4]
    cwd_parts.append(cwd_parts[3])
    project_root = os.sep.join(cwd_parts)
    return project_root

def get_lint_config_file():
    """Retrieve location of pylintrc config file."""
    project_root = get_project_root_directory()
    parts = project_root.split(os.sep)
    parts = parts[:4]
    parts.append("tools")
    parts.append("qa.pylintrc")
    result = os.sep.join(parts)
    return result

def pylint_evaluation(target):
    """Run pylint evaluation in new process."""
    config = get_lint_config_file()
    arguments = ["pylint", "--rcfile", config, target]
    result = subprocess.run(arguments, stdout=subprocess.PIPE)
    result = result.stdout.decode("ascii")
    return result

def pydoc_evaluation(target):
    """Run pydoc evaluation in new process."""
    result = subprocess.run(["pydocstyle", target], stdout=subprocess.PIPE)
    result = result.stdout.decode("ascii")
    return result

def _main_routine():
    """Entry point for command line usage."""
    command_arguments = sys.argv[1:]
    target = command_arguments[0]
    if not target_is_in_cwd(target):
        project_root = get_project_root_directory()
        target = find_target_in_project(project_root, target)
    if target == "":
        print("Target not found in project directories.")
        sys.exit()
    pydoc_eval = pydoc_evaluation(target)
    pylint_eval = pylint_evaluation(target)
    print(pydoc_eval)
    print(pylint_eval)

if __name__ == "__main__":
    _main_routine()
