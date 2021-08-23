import os
import fire
import subprocess

from loguru import logger as logging


class Rocket:
    _python_executable = 'python3'
    _interval_repeat_watch = 3
    # in seconds
    """rocket main executable"""
    def trigger(self, project_location: str, dbfs_path: str, watch=False):
        """
        :param project_location:
        :param dbfs_folder: path where the wheel will be stored, ex: dbfs:/tmp/myteam/myproject
        :return:
        """

        self.project_location = project_location
        project_directory = os.path.dirname(project_location)
        project_directory = project_directory[:-1]

        self.dbfs_folder = dbfs_path + project_directory

        if watch:
            self._build_and_deploy()
            from time import sleep; sleep(self._interval_repeat_watch)
            return self._watch()

        return self._build_and_deploy()

    def _build(self):
        """ builds a library with that project"""

        if not os.path.exists(f"{self.project_location}/setup.py"):
            raise Exception("To be turned into a library your project has to contain a setup.py file")

        dist_location = f"{self.project_location}/dist"
        # cleans up dist
        self._shell(f"rm {dist_location}/* || true")

        self._shell(f"cd {self.project_location} ; {self._python_executable} -m build")
        self.wheel_file = self._shell(f"cd {dist_location}; ls *.whl | head -n 1").replace("\n", "")
        self.wheel_path = f"{dist_location}/{self.wheel_file}"
        logging.info(f"Build Successful. Wheel: '{self.wheel_path}' ")

    def _deploy(self):
        """Deploys the version specified in config.yml"""
        self._shell(
            f"databricks fs cp --overwrite {self.wheel_path} {self.dbfs_folder}/{self.wheel_file}"
        )

        print(f"""
Great! in your notebook install the library by running:

%pip install {self.dbfs_folder.replace("dbfs:/","/dbfs/")}/{self.wheel_file} --force-reinstall

If you are running spark 6 use this command instead (and clean the state before a new version):

dbutils.library.install('{self.dbfs_folder}/{self.wheel_file}'); dbutils.library.restartPython()

        """)

    def _watch(self):
        cmd = f"watchmedo shell-command -w -W --interval {self._interval_repeat_watch} --patterns='*.py' --ignore-pattern='*build*;*egg-info*;*dist*'" \
              f" --recursive " \
              f"--command='rocket " \
              f"trigger " \
              f"{self.project_location} {self.dbfs_folder}' {self.project_location}"
        logging.info(f'watch command: {cmd}')
        print(os.system(cmd))

    def _send_notification(self, message):
        os.system(f"notify-send '{message}'")

    def _build_and_deploy(self):
        logging.info("Starting to build")
        self._build()
        result = self._deploy()
        return result


    @staticmethod
    def _shell(cmd) -> str:
        logging.info(f"Running shell command: {cmd} ")
        return subprocess.check_output(cmd, shell=True).decode("utf-8")


def main():
    fire.Fire(Rocket)
