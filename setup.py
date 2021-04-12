import setuptools

setuptools.setup(
    name="databricks-rocket",
    version="0.0.1",
    author="GetYourGuide",
    author_email="engineering.data-products@getyourguide.com",
    description="Move code from your local machine to use in databricks during development",
    url="https://github.com/getyourguide/databricks-rocket",
    packages=setuptools.find_packages(),
    install_requires=["loguru", "fire", "watchdog"],
    entry_points={
        'console_scripts': [
            'rocket=databricks_local.databricks_local:main'
        ]
    }
)
