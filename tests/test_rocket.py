import unittest

from rocket.rocket import Rocket


def test_build_python(python_rocket: Rocket):
    """
    Test if DB Rocket can build a python project
    """
    python_rocket._build()
    assert python_rocket.wheel_file
    assert python_rocket.wheel_path


def test_build_poetry(poetry_rocket: Rocket):
    """
    Test if DB Rocket can build a poetry project
    """
    poetry_rocket._build()
    assert poetry_rocket.wheel_file
    assert poetry_rocket.wheel_path


def test_build_raises_error():
    """
    Test if DB Rocket will raise an error if project is not a supported project
    """
    rocket = Rocket()
    rocket.project_location = "/tmp"

    try:
        rocket._build()
    except:
        assert True

    assert not hasattr(rocket, "wheel_file")
    assert not hasattr(rocket, "wheel_path")


if __name__ == "__main__":
    unittest.main()
