
The purpose of this library is to make it easy to develop Models in the local machine.


## Installing



```sh
pip install git+ssh://git@github.com/getyourguide/databricks-local.git
```


## Deploy python project in a notebook with watch enabled


To deploy a python project

```sh
db_local build_and_deploy project_directory dbfs:/temp/rnr-test/conduction_time_predictor --enable-watch=True

```

This command will return the exact command you have to perform in your notebook next:

Create a cell in the top of the notebook and paste the content (example below)

```sh
%pip install dbfs:/temp/rnr-test/conduction_time_predictor/conduction_time_predictor-0.0.1-py3-none-any.whl
```

