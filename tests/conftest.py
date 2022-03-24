import os

import pytest as pytest

from rocket.rocket import Rocket


@pytest.fixture()
def python_rocket() -> Rocket:
    rocket = Rocket()
    test_dir = os.path.dirname(os.path.realpath(__file__))
    project_path = os.path.join(test_dir, "resources", "python-test")
    rocket.project_location = project_path
    return rocket


@pytest.fixture()
def poetry_rocket() -> Rocket:
    rocket = Rocket()
    test_dir = os.path.dirname(os.path.realpath(__file__))
    project_path = os.path.join(test_dir, "resources", "poetry-test")
    rocket.project_location = project_path
    return rocket
