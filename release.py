#!/usr/bin/env python3

import os


class Release:
    """
    Class responsible to serve the library in pypi, not part of rocket executable
    """

    """Module responsible for building db-rocket itself and publishing it to pypi"""

    def release(self):
        """
        Build rocket for pypi doing all steps. Run it on the root of rocket project.
        """
        os.system("rm -rf dist/* || true")
        os.system("python3 -m build --no-isolation")
        self.build()
        self.upload()

    def build(self):
        """
        Build rocket for pypi. Run it on the root of rocket project.
        """
        os.system("rm -rf dist/* || true")
        os.system("python3 -m build --no-isolation")
        print("Build successfull, uploading now")

    def upload(self):
        """
        Upload new package to pipy
        :return:
        """
        os.system("python3 -m twine upload dist/*")


if __name__ == "__main__":
    import fire

    fire.Fire(Release)
