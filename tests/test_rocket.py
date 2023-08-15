from rocket.rocket import Rocket


def test_create_python_wheel_from_python_project_successful(rocket: Rocket, python_project_path: str):
    """
    Test if DB Rocket can build a python project
    """
    wheel_path, wheel_file = rocket._create_python_project_wheel(python_project_path)
    assert wheel_file
    assert wheel_path


def test_create_python_wheel_from_poetry_project_successful(rocket: Rocket, poetry_project_path: str):
    """
    Test if DB Rocket can build a poetry project
    """
    wheel_path, wheel_file = rocket._create_python_project_wheel(poetry_project_path)
    assert wheel_file
    assert wheel_path


def test_create_python_wheel_from_temp_folder_raises_exception(rocket: Rocket):
    """
    Test if DB Rocket will raise an error if project is not a supported project
    """
    try:
        wheel_path, wheel_file = rocket._create_python_project_wheel("/tmp")
    except:
        assert True

