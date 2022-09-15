import unittest

from rocket.rocket import Rocket, _add_index_urls_to_cmd


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


def test_add_index_urls_to_cmd():
    dummy_cmd = "test_cmd"
    dummy_index_urls = ["dummy_index"]

    assert _add_index_urls_to_cmd(dummy_cmd, dummy_index_urls) == "dummy_index test_cmd"


def test_add_index_urls_to_cmd_without_urls():
    dummy_cmd = "test_cmd"
    dummy_index_urls = []

    assert _add_index_urls_to_cmd(dummy_cmd, dummy_index_urls) == "test_cmd"


if __name__ == "__main__":
    unittest.main()
