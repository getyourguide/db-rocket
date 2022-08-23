import os
import subprocess
import sys
from typing import Optional


import fire

from rocket.logger import configure_logger

logger = configure_logger()


class Rocket:
    """Entry point of the installed program, all public methods are options of the program"""

    # in seconds
    _interval_repeat_watch: int = 2
    _python_executable: str = "python3"
    _rocket_executable: str = "rocket"

    def __init__(self):
        if os.getenv("DATABRICKS_TOKEN") is None:
            raise Exception("DATABRICKS_TOKEN must be set for db-rocket to work")

    def setup(self):
        """
        Initialize the application.
        """
        if os.path.exists("setup.py") or os.path.exists(f"pyproject.toml"):
            print("Packaing file already exists so no need to create a new one")
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


        print("Setup.py file created, feel free to modify it with your needs.")

    def trigger(
        self, project_location: str = ".", dbfs_path: Optional[str] = None, watch=True, disable_watch=False
    ):
        """
        Entrypoint of the application, triggers a build and deploy
        :param project_location:
        :param dbfs_folder: path where the wheel will be stored, ex: dbfs:/tmp/myteam/myproject
        :return:
        """
        if not dbfs_path:
            dbfs_path = f"dbfs:/temp/{os.environ['USER']}"

        self.project_location = project_location
        project_directory = os.path.dirname(project_location)
        project_directory = project_directory[:-1]

        self.dbfs_folder = dbfs_path + project_directory

        if watch and not disable_watch:
            # first time build and then watch so we have an immediate build
            self._build_and_deploy()
            return self._watch()
        else:
            logger.debug("Watch disabled")

        return self._build_and_deploy()

    def _build_and_deploy(self):
        self._build()
        result = self._deploy()
        return result

    def _watch(self) -> None:
        """
        Listen to filesystem changes to trigger again
        """
        command_list = sys.argv
        # disable watch takes precedence over --enable
        command_list.append("--disable_watch=True")
        command = " ".join(command_list)

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
        os.system(cmd)

    def _deploy(self):
        """
        Copies the built library to dbfs
        """

        try:
            self._shell(
                f"databricks fs cp --overwrite {self.wheel_path} {self.dbfs_folder}/{self.wheel_file}"
            )
        except Exception as e:
            raise Exception(
                f"Error while copying files to databricks, is your DATABRICKS_TOKEN set and valid? Details follow {e}"
            )

        print(
            f"""Great! in your notebook install the library by running:
            
%pip install --upgrade pip
%pip install {self.dbfs_folder.replace("dbfs:/", "/dbfs/")}/{self.wheel_file} --force-reinstall
        """
        )

    def _build(self):
        """
        builds a library with that project
        """
        logger.info("Building your Python repo as a library")

        # cleans up dist folder from previous build
        dist_location = f"{self.project_location}/dist"
        self._shell(f"rm {dist_location}/* 2>/dev/null || true")

        if os.path.exists(f"{self.project_location}/setup.py"):
            self._shell(
                f"cd {self.project_location} ; {self._python_executable} -m build --outdir {dist_location} 2>/dev/null"
            )
        elif os.path.exists(f"{self.project_location}/pyproject.toml"):
            self._shell(f"cd {self.project_location} ; poetry build --format wheel")
        else:
            raise Exception(
                "To be turned into a library your project has to contain a setup.py or pyproject.toml file"
            )

        self.wheel_file = self._shell(
            f"cd {dist_location}; ls *.whl 2>/dev/null | head -n 1"
        ).replace("\n", "")
        self.wheel_path = f"{dist_location}/{self.wheel_file}"
        logger.debug(f"Build Successful. Wheel: '{self.wheel_path}' ")

    @staticmethod
    def _shell(cmd) -> str:
        logger.debug(f"Running shell command: {cmd} ")
        return subprocess.check_output(cmd, shell=True).decode("utf-8")

def main():
    fire.Fire(Rocket)
