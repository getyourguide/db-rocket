import setuptools

setuptools.setup(
    name="databricks-local",
    version="0.0.1",
    author="Jean Carlo Machado",
    author_email="jean.machado@getyourguide.com",
    description="Move code from your local machine to use in databricks during development",
    url="https://github.com/getyourguide/databricks-local",
    packages=setuptools.find_packages(),
    install_requires=["loguru", "fire", "watchdog"],
    entry_points={
        'console_scripts': [
            'db_local=databricks_local.databricks_local:main'
        ]
    }
)
