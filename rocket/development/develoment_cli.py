from rocket.rocket import Rocket
from rocket.development.self_release import SelfRelease


class Cli:
    """
    Cli used for developing db-rocket. The real binary exported during installation is rocket

    """
    def __init__(self):
        self.rocket = Rocket
        self.self_release = SelfRelease