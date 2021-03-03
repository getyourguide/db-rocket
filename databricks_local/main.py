import os
import fire

from loguru import logger as logging

class DatabricksLocal:
    def __init__(self):
        pass

    def build_and_deploy(self, project_location: str, dbfs_folder: str):
        """
        :param project_location:
        :param dbfs_folder: path where the wheel will be stored, ex: dbfs:/tmp/myteam/myproject
        :return:
        """
        self.project_location = project_location
        self.dbfs_folder = dbfs_folder

        self._build()
        return self._deploy()

    def _build(self):
        """ builds a library with that project"""

        dist_location = f"{self.project_location}/dist"
        #cleans up dist
        self._execute(f"rm {dist_location}/*")

        self._execute(f"cd {self.project_location} ; python setup.py bdist_wheel")
        self.wheel_file = self._execute(f"ls {dist_location} | head -n 1").replace("\n", "")
        self.wheel_path = f"{dist_location}/{self.wheel_file}"
        logging.info(f"Build Successful. Wheel: '{self.wheel_path}' ")


    def _deploy(self):
        """Deploys the version specified in config.yml"""
        self._execute(
            f"databricks fs cp --overwrite {self.wheel_path} {self.dbfs_folder}/{self.wheel_file}"
        )

        return f"""
Great! in your notebook install the library by running: 

%pip install {self.dbfs_folder}/{self.wheel_file}
        """

    def watch_and_deploy(self):
        os.system('''
            watchmedo shell-command --patterns="*.py" --recursive --command='./cli.py mlservice build_and_deploy' conduction_time
        ''')

    def list_deployed(self):
        self._execute(f"databricks fs ls {self.directory_to_deploy_in}")


    def perform(self):
        self.build_and_deploy()

    def install_db_connect(self):
        import os
        os.system("pip uninstall pyspark; pip install 'databricks-connect==7.3.9' ")
        #os.system("dbconnect configure")
        return "Great, now to test the configuration run: databricks-connect test"


    @staticmethod
    def _execute(cmd) -> str:
        logging.info(f"Runnimng command: {cmd} ")
        import subprocess
        return subprocess.check_output(cmd, shell=True).decode("utf-8")

def main():
    fire.Fire(DatabricksLocal)