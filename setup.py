import setuptools

setuptools.setup(
    name="databricks-rocket",
    version="0.9.3",
    author="GetYourGuide",
    author_email="engineering.data-products@getyourguide.com",
    description="Keep your local python scripts installed and in sync with a databricks notebook. Shortens the feedback loop to develop projects using a hybrid enviroment",
    url="https://github.com/getyourguide/databricks-rocket",
    packages=setuptools.find_packages(),
    install_requires=["loguru", "fire", "watchdog", "argh", "build", "pyyaml"],
    entry_points={
        'console_scripts': [
            'rocket=rocket.main:main'
        ]
    }
)
