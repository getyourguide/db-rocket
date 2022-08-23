import setuptools

setuptools.setup(
    name="databricks-rocket",
    version="1.1.0",
    author="GetYourGuide",
    author_email="engineering.data-products@getyourguide.com",
    description="Keep your local python scripts installed and in sync with a databricks notebook. Shortens the feedback loop to develop projects using a hybrid enviroment",
    url="https://github.com/getyourguide/databricks-rocket",
    packages=setuptools.find_packages(),
    install_requires=["fire", "watchdog", "build", 'databricks_cli'],
    entry_points={"console_scripts": ["rocket=rocket.rocket:main","dbrocket=rocket.rocket:main"]},
)
