import unittest

from rocket.rocket import Rocket


def test_build_python(python_rocket):
    python_rocket._build()
    assert python_rocket.wheel_file
    assert python_rocket.wheel_path


def test_build_poetry(poetry_rocket):
    poetry_rocket._build()
    assert poetry_rocket.wheel_file
    assert poetry_rocket.wheel_path


def test_build_wrong_project_location():
    rocket = Rocket()
    rocket.project_location = "/tmp"

    try:
        rocket._build()
    except:
        assert True

    assert not hasattr(rocket, 'wheel_file')
    assert not hasattr(rocket, 'wheel_path')


if __name__ == '__main__':
    unittest.main()
