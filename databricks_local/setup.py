from loguru import logger as logging

class Setup:
    def databricks_connect(self, project_name):
        self._execute_each([
            f"conda create --name {project_name}-dbconnect --clone {project_name}",
            "pip uninstall pyspark",
            "pip install 'databricks-connect==7.3.9'",
            "databricks-connect configure",
            "databricks-connect test",
        ], dry_run=True)

    @staticmethod
    def _execute_each(entries, dry_run=False) -> str:
        for entry in entries:
            if dry_run:
                print(entry)
            else:
                Setup.shell(entry)

    @staticmethod
    def _shell(cmd) -> str:
        logging.info(f"Running shell command: {cmd} ")
        return subprocess.check_output(cmd, shell=True).decode("utf-8")

