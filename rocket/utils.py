import concurrent.futures
import os
import subprocess

from rocket.logger import logger


def execute_for_each_multithreaded(lst, func, max_threads=None):
    """
    Execute a given function for each entry in the list using multiple threads.

    Parameters:
    - lst: List of items to process
    - func: Function to apply to each item
    - max_threads: Maximum number of threads to use (default is None, which means as many as items in the list)

    Returns:
    - List of results after applying the function
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        return list(executor.map(func, lst))


def extract_package_name_from_wheel(wheel_filename):
    # Split the filename on '-' and take the first part
    return wheel_filename.split("-")[0]


def extract_project_name_from_wheel(wheel_filename):
    return extract_package_name_from_wheel(wheel_filename).replace("_", "-")


def extract_python_package_dirs(root_dir):
    packages = []
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path) and "__init__.py" in os.listdir(item_path):
            packages.append(item_path)
    return packages


def execute_shell_command(cmd) -> str:
    logger.debug(f"Running shell command: {cmd} ")
    return subprocess.check_output(cmd, shell=True).decode("utf-8")


def extract_python_files_from_folder(path):
    py_files = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))

    return py_files
