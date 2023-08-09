import os
from typing import Optional

import fire

from rocket.logger import logger
from rocket.utils import execute_shell_command, extract_project_name_from_wheel, \
    extract_package_name_from_wheel


def _add_index_urls_to_cmd(cmd, index_urls):
    if index_urls:
        return f"{' '.join(index_urls)} {cmd}"
    else:
        return cmd


class Rocket:
    """Entry point of the installed program, all public methods are options of the program"""

    # in seconds
    _interval_repeat_watch: int = 2
    _python_executable: str = "python3"
    _rocket_executable: str = "rocket"

    def setup(self):
        """
        Initialize the application.
        """
        if os.path.exists("setup.py") or os.path.exists(f"pyproject.toml"):
            logger.info("Packaing file already exists so no need to create a new one")
            return

        content = """
import setuptools

setuptools.setup(
    name="myproject",
    version="0.0.1",
    author="",
    author_email="",
    description="",
    url="https://github.com/getyourguide/databricks-rocket",
    packages=setuptools.find_packages(),
)
        """

        with open("setup.py", "a") as myfile:
            myfile.write(content)
        logger.info("Setup.py file created, feel free to modify it with your needs.")

    def launch(
            self,
            project_location: str = ".",
            dbfs_path: Optional[str] = None,
            watch=True,
    ):
        """
        Entrypoint of the application, triggers a build and deploy
        :param project_location:
        :param dbfs_path: path where the wheel will be stored, ex: dbfs:/tmp/myteam/myproject
        :param watch: Set to false if you don't want to automatically sync your files
        :return:
        """

        if os.getenv("DATABRICKS_TOKEN") is None:
            raise Exception("DATABRICKS_TOKEN must be set for db-rocket to work")

        if not dbfs_path:
            dbfs_path = f"dbfs:/temp/{os.environ['USER']}"

        self.project_location = project_location
        project_directory = os.path.dirname(project_location)
        project_directory = project_directory[:-1]

        self.dbfs_folder = dbfs_path + project_directory

        if watch:
            self._build_and_deploy()
            return self._watch(
                f'rocket launch --project_location={project_location} --watch=False --dbfs_path={dbfs_path}')

        return self._build_and_deploy()

    def _build_and_deploy(self):
        self._build()
        result = self._deploy()
        return result

    def _watch(self, command) -> None:
        """
        Listen to filesystem changes to trigger again
        """
        cmd = f"""watchmedo \
                shell-command \
                --patterns='*.py'  \
                --wait --drop \
                --interval {self._interval_repeat_watch} \
                --debug-force-polling \
                --ignore-directories \
                --ignore-pattern '*.pyc;*dist*;\..*;*egg-info' \
                --recursive  \
                --command='{command}' 
              """
        logger.debug(f"watch command: {cmd}")
        execute_shell_command(cmd)

    def _deploy(self):
        """
        Copies the built library to dbfs
        """

        try:
            execute_shell_command(
                f"databricks fs cp --overwrite {self.wheel_path} {self.dbfs_folder}/{self.wheel_file}"
            )
            package_name = extract_package_name_from_wheel(self.wheel_file)
            execute_shell_command(
                f"databricks fs cp --recursive --overwrite {self.project_location}/{package_name} {self.dbfs_folder}/{package_name}"
            )
        except Exception as e:
            raise Exception(
                f"Error while copying files to databricks, is your databricks token set and valid? Try to generate a new token and update existing one with `databricks configure --token`. Error details: {e}"
            )

        base_path = self.dbfs_folder.replace("dbfs:/", "/dbfs/")
        install_cmd = f'{base_path}/{self.wheel_file}'
        install_cmd = _add_index_urls_to_cmd(install_cmd, self.index_urls)
        project_name = extract_project_name_from_wheel(self.wheel_file)

        logger.info(
            f"""Install your library in your databricks notebook by running:
%pip install --upgrade pip
%pip install {install_cmd} --force-reinstall


If you have watch activated, your project will be automatically synchronised with databricks. To utilise it, add following in one cell:
%pip install --upgrade pip
%pip install {install_cmd} --force-reinstall
%pip uninstall -y {project_name}

and then in new Python cell:
%load_ext autoreload
%autoreload 2
import sys
import os
sys.path.append(os.path.abspath('{base_path}')
""")

    def _build(self):
        """
        builds a library with that project
        """
        logger.info("We are now building your Python repo as a library...")

        # cleans up dist folder from previous build
        dist_location = f"{self.project_location}/dist"
        execute_shell_command(f"rm {dist_location}/* 2>/dev/null || true")

        if os.path.exists(f"{self.project_location}/setup.py"):
            logger.info("Found setup.py. Building python library")
            execute_shell_command(
                f"cd {self.project_location} ; {self._python_executable} -m build --outdir {dist_location} 2>/dev/null"
            )
            self.index_urls = []
            if os.path.exists(f"{self.project_location}/requirements.txt"):
                with open(f"{self.project_location}/requirements.txt") as f:
                    self.index_urls = [line.strip() for line in f.readlines() if "index-url" in line]

        elif os.path.exists(f"{self.project_location}/pyproject.toml"):
            logger.info("Found pyproject.toml. Building python library with poetry")
            execute_shell_command(f"cd {self.project_location} ; poetry build --format wheel")
            requirements = execute_shell_command(
                f"cd {self.project_location} ; poetry export --with-credentials --without-hashes")
            self.index_urls = [line.strip() for line in requirements.split("\n") if "index-url" in line]
        else:
            raise Exception(
                "To be turned into a library your project has to contain a setup.py or pyproject.toml file"
            )

        self.wheel_file = execute_shell_command(
            f"cd {dist_location}; ls *.whl 2>/dev/null | head -n 1"
        ).replace("\n", "")
        self.wheel_path = f"{dist_location}/{self.wheel_file}"
        logger.debug(f"Build Successful. Wheel: '{self.wheel_path}' ")


def main():
    fire.Fire(Rocket)
