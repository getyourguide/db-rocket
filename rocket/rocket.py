import logging
import os
import subprocess
import sys

import fire


def configure_logger() -> logging.Logger:
    logger = logging.getLogger("dbrocket")
    logger.addHandler(logging.StreamHandler(sys.stdout))
    # use this for debug purposes
    # logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)
    return logger


logger = configure_logger()


class Rocket:
    """ Entry point of the installed program, all public methods are options of the program"""

    # in seconds
    _interval_repeat_watch: int = 2
    _python_executable: str = "python3"
    _rocket_executable: str = "rocket"

    def trigger(
        self, project_location: str, dbfs_path: str, watch=True, disable_watch=False
    ):
        """
        Entrypoint of the application, triggers a build and deploy
        :param project_location:
        :param dbfs_folder: path where the wheel will be stored, ex: dbfs:/tmp/myteam/myproject
        :return:
        """

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
        self._shell(
            f"databricks fs cp --overwrite {self.wheel_path} {self.dbfs_folder}/{self.wheel_file}"
        )

        print(
            f"""Great! in your notebook install the library by running:

    %pip install {self.dbfs_folder.replace("dbfs:/","/dbfs/")}/{self.wheel_file} --force-reinstall

Or if you are running spark 6 use this command instead (and clean the state before a new version):

    dbutils.library.install('{self.dbfs_folder}/{self.wheel_file}')
    dbutils.library.restartPython()

        """
        )

    def _build(self):
        """
        builds a library with that project
        """
        logger.info("Building your python repo as a library")

        if not os.path.exists(f"{self.project_location}/setup.py"):
            raise Exception(
                "To be turned into a library your project has to contain a setup.py file"
            )

        dist_location = f"/tmp/db_rocket_builds"
        # cleans up dist folder from previous build
        self._shell(f"rm {dist_location}/* 2>/dev/null || true")

        self._shell(
            f"cd {self.project_location} ; {self._python_executable} -m build --outdir {dist_location}"
        )
        self.wheel_file = self._shell(
            f"cd {dist_location}; ls *.whl | head -n 1"
        ).replace("\n", "")
        self.wheel_path = f"{dist_location}/{self.wheel_file}"
        logger.debug(f"Build Successful. Wheel: '{self.wheel_path}' ")

    def _send_notification(self, message) -> None:
        os.system(f"notify-send '{message}'")

    @staticmethod
    def _shell(cmd) -> str:
        logger.debug(f"Running shell command: {cmd} ")
        return subprocess.check_output(cmd, shell=True).decode("utf-8")

    def _hello(self):
        print(
            """
        Greetings from db-rocket :)
        Version 2n
        """
        )


def main():
    fire.Fire(Rocket)
