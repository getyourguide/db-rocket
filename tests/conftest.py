import os

import pytest as pytest

from rocket.rocket import Rocket


@pytest.fixture()
def python_project_path() -> str:
    test_dir = os.path.dirname(os.path.realpath(__file__))
    project_path = os.path.join(test_dir, "resources", "python-test")
    return project_path


@pytest.fixture()
def poetry_project_path() -> str:
    test_dir = os.path.dirname(os.path.realpath(__file__))
    project_path = os.path.join(test_dir, "resources", "poetry-test")
    return project_path


@pytest.fixture()
def rocket() -> Rocket:
    rocket = Rocket()
    return rocket
