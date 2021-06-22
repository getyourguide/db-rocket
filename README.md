![image](https://user-images.githubusercontent.com/2252355/118677158-5293ed80-b7fc-11eb-9619-e98829bbc9ce.png)

[![PyPI version](https://badge.fury.io/py/databricks-rocket.svg)](https://badge.fury.io/py/databricks-rocket)
![PyPI downloads](https://img.shields.io/pypi/dm/databricks-rocket)

Keep your local python scripts installed and in sync with a databricks notebook.
Every change on your local machine is automatically applied to the notebook.
Shortens the feedback loop to develop git based projects.
Removes the need to setup a local development environment.


## Installing

For a clean python installation (specially on MacOs) we recommend [using conda](docs/conda.md)

```sh
pip install databricks-rocket
```

For the library to work you need [databricks-cli](https://pypi.org/project/databricks-cli) configured with a valid token.
If you haven't done so yet just run the commands below and follow the instructions:

```sh
pip install databricks-cli
databricks configure --token
```

### Troubleshooting

On MacOs, also upgrade the build library:

```sh
python3 -m pip install --upgrade build 
```

## Using


To deploy any python project *with a setup.py*

```sh
# enter the project you want to install in the notebook and run the following command
rocket trigger . dbfs:/temp/your_name --watch=True
# you can you any path here but we recommend namespacing it with your name
```

This command will return the exact command you have to perform in your notebook next:

Create a cell in the top of the notebook and paste the content (example below)

```sh
%pip install /dbfs/temp/your_folder/your-package0.0.1-py3-none-any.whl  --force-reinstall --no-deps 
```

## Support

- Databricks: 7 (recommended), 6.4 (supported but requires cleaning the notebook state)  
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
