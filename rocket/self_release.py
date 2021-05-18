import os

class SelfRelease:
    """Module responsible for building db-rocket itself and publishing it to pypi"""
    def build(self):
        """
        Build rocket for pypi. Run it on the root of rocket project.
        """
        os.system("rm -rf dist/* || true")
        os.system("python3 -m build")


    def release(self):
        """
        Build rocket for pypi. Run it on the root of rocket project.
        """
        os.system("rm -rf dist/* || true")
        os.system("python3 -m build")
        os.system("python3 -m twine upload dist/*")

