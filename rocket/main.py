import os
import fire
import sys
import subprocess

from loguru import logger as logging
import time

from rocket.setup import Setup


class Rocket:
    def __init__(self):
        self.setup = Setup

    def trigger(self, project_location: str, dbfs_path: str, enable_watch=False):
        """
        :param project_location:
        :param dbfs_folder: path where the wheel will be stored, ex: dbfs:/tmp/myteam/myproject
        :return:
        """

        self.project_location = project_location
        project_directory = os.path.dirname(project_location)
        project_directory = project_directory[:-1]

        self.dbfs_folder = dbfs_path + project_directory

        if enable_watch:
            return self._watch()

        return self._build_and_deploy()

    def _build(self):
        """ builds a library with that project"""

        if not os.path.exists(f"{self.project_location}/setup.py"):
            raise Exception("To be turned into a library your project has to contain a setup.py file")

        dist_location = f"{self.project_location}/dist"
        # cleans up dist
        self._shell(f"rm {dist_location}/* || true")

        self._shell(f"cd {self.project_location} ; python -m build")
        self.wheel_file = self._shell(f"ls {dist_location} | head -n 1").replace("\n", "")
        self.wheel_path = f"{dist_location}/{self.wheel_file}"
        logging.info(f"Build Successful. Wheel: '{self.wheel_path}' ")

    def _deploy(self):
        """Deploys the version specified in config.yml"""
        self._shell(
            f"databricks fs cp --overwrite {self.wheel_path} {self.dbfs_folder}/{self.wheel_file}"
        )

        return f"""
Great! in your notebook install the library by running:


%pip install {self.dbfs_folder.replace("dbfs:/","/dbfs/")}/{self.wheel_file} --force-reinstall --no-deps

If you are dunning spark < 7 use this command:

        """

    def _watch(self):
        cmd = f"watchmedo shell-command -w -W --interval 3 --patterns='*.py' --ignore-pattern='*build*'" \
              f" --recursive " \
              f"--command='db_local " \
              f"build_and_deploy " \
              f"{self.project_location} {self.dbfs_folder}' {self.project_location}"
        logging.info(f'watch command: {cmd}')
        print(os.system(cmd))

    def _send_notification(self, message):
        os.system(f"notify-send '{message}'")

    def _build_and_deploy(self):
        logging.info("Starting to build")
        self._build()
        result = self._deploy()
        #self._send_notification("Deploy finished successfully")
        return result


    @staticmethod
    def _shell(cmd) -> str:
        logging.info(f"Running shell command: {cmd} ")
        return subprocess.check_output(cmd, shell=True).decode("utf-8")

    def build_self(self):
        """
        Build rocket for pypi. Run it on the root of rocket project.
        """
        os.system("rm -rf dist/* || true")
        os.system("python3 -m build")
        os.system("python3 -m twine upload dist/*")


def main():
    fire.Fire(Rocket)
