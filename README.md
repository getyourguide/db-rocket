
The purpose of this library is to make it easy to develop Models in the local machine.



## Running python projects in a notebook


To deploy a project

```sh
db_local build_and_deploy project_directory dbfs:/temp/rnr-test/conduction_time_predictor

```

This command will return the exact command you have to perform in your notebook next:

Create a cell and type the content:

```sh
%pip install dbfs:/temp/rnr-test/conduction_time_predictor/conduction_time_predictor-0.0.1-py3-none-any.whl
```

