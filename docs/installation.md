
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
