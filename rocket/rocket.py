import os
import fire
import subprocess
import logging
import sys


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
    _interval_repeat_watch : int = 3
    _python_executable : str = 'python3'
    _rocket_executable : str = 'rocket'


    """rocket main executable"""
    def trigger(self, project_location: str, dbfs_path: str, watch=False):
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

        if watch:
            # first time build and then watch so we have an immediate build
            self._build_and_deploy()
            from time import sleep; sleep(self._interval_repeat_watch)
            return self._watch()

        return self._build_and_deploy()

    def _build(self):
        """
        builds a library with that project
        """
        logger.info("Building python library")

        if not os.path.exists(f"{self.project_location}/setup.py"):
            raise Exception("To be turned into a library your project has to contain a setup.py file")

        dist_location = f"{self.project_location}/dist"
        # cleans up dist folder from previous build
        self._shell(f"rm {dist_location}/* 2>/dev/null || true")

        self._shell(f"cd {self.project_location} ; {self._python_executable} -m build ")
        self.wheel_file = self._shell(f"cd {dist_location}; ls *.whl | head -n 1").replace("\n", "")
        self.wheel_path = f"{dist_location}/{self.wheel_file}"
        logger.debug(f"Build Successful. Wheel: '{self.wheel_path}' ")

    def _deploy(self):
        """
        Copies the built library to dbfs
        """
        self._shell(
            f"databricks fs cp --overwrite {self.wheel_path} {self.dbfs_folder}/{self.wheel_file}"
        )

        print(f"""Great! in your notebook install the library by running:

%pip install {self.dbfs_folder.replace("dbfs:/","/dbfs/")}/{self.wheel_file} --force-reinstall

If you are running spark 6 use this command instead (and clean the state before a new version):

dbutils.library.install('{self.dbfs_folder}/{self.wheel_file}'); dbutils.library.restartPython()

        """)

    def _watch(self) -> None:
        """
        Listen to filesystem changes to build and deploy again
        """
        def get_command_without_watch() -> str:
            """
            Send to the watch command the command without the watch flag otherwise an infinite loop will be triggered
            """
            command = sys.argv
            watch_flag = '--watch=True'
            if watch_flag in command:
                command.remove(watch_flag)
            command = ' '.join(command)
            logging.debug(command)
            return command


        cmd = f"""watchmedo \
                shell-command \
                --wait --drop  \
                --patterns='*.py'  \
                --recursive  \
                --ignore-patterns '*/.*;build;*.egg-info;*dist' \
                --command='{get_command_without_watch()}' 
              """
        logger.debug(f'watch command: {cmd}')
        logger.debug(os.system(cmd))

    def _send_notification(self, message) -> None:
        os.system(f"notify-send '{message}'")

    def _build_and_deploy(self):
        self._build()
        result = self._deploy()
        return result

    @staticmethod
    def _shell(cmd) -> str:
        logger.debug(f"Running shell command: {cmd} ")
        return subprocess.check_output(cmd, shell=True).decode("utf-8")


def main():
    fire.Fire(Rocket)
