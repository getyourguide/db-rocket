## DB-Rocket

<img src="https://user-images.githubusercontent.com/2252355/173396060-8ebb3a33-f389-421d-bea4-afc01a078307.svg" width="100" height="100">

[![PyPI version](https://badge.fury.io/py/databricks-rocket.svg)](https://badge.fury.io/py/databricks-rocket)
![PyPI downloads](https://img.shields.io/pypi/dm/databricks-rocket)

Keep your local python scripts installed and in sync with a databricks notebook.
Every change on your local machine is automatically applied to the notebook.
Shortens the feedback loop to develop git based projects.
Removes the need to setup a local development environment.

Find installation instructions [here](docs/installation.md).

## Using

To deploy any python project *with a setup.py*

```sh
rocket trigger {local_project_directory} dbfs:{directory_to_install_in_dbfs}
```

Example:

![img.png](img.png =250x250)

The command returns the exact command you have to perform in your notebook next.
Create a cell in a notebook and paste the content (example below).

![img_1.png](img_1.png)

## Support

- Databricks: >=7
- Python: >=3.7
- Tested on Platform: Linux, MacOs. Windows will probably not work but contributions are welcomed!

## Acknowledgments

- Thanks Leon Poli for the Logo :)
- Thanks Stephane Leonard for source-code and documentation improvements :)
- Thanks Malachi Soord for the CICD setup and README improvements

Contributions are welcomed!

# Security

For security issues please contact [security@getyourguide.com](mailto:security@getyourguide.com).

# Legal

db-rocket is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE.txt) for the full text.
