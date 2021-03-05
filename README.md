The purpose of this project is to keep local python libraries in sync in a notebook. 
Every change in your local machine directly applied to the notebook.

## Installing


```sh
pip install git+ssh://git@github.com/getyourguide/databricks-local.git
```


For the library to work you need databricks-cli configured.
If you havent done so you, just run:

```sh
 databricks configure --token
```

## Deploy python project and use in notebook


To deploy any python project with a setup.py

```sh
db_local build_and_deploy local_project_directory dbfs:/temp/your_folder
```

This command will return the exact command you have to perform in your notebook next:

Create a cell in the top of the notebook and paste the content (example below)

```sh
%pip install /dbfs/temp/your_folder/your-package0.0.1-py3-none-any.whl  --force-reinstall --no-deps
```

To keep tracking any file changes add the parameter `--enable-watch=True` to the build_and_deploy command.



Contributions are welcomed!

