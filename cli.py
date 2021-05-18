#!/usr/bin/env python

import fire
from rocket.main import Rocket
from rocket.self_release import SelfRelease


class Cli:
    """
    Cli used for developing db-rocket. The real binary exported during installation is rocket

    """
    def __init__(self):
        self.rocket = Rocket
        self.self_release = SelfRelease

if __name__ == "__main__":
    fire.Fire(Cli)
