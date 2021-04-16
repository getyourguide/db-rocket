The purpose of this project is to keep a Databricks notebook synced with local python libraries. 
Every change on your local machine is directly applied to the notebook.

## Installing locally


```sh
pip install databricks-rocket
```


For the library to work you need databricks-cli configured with a valid token.
If you haven't done so you, just run:

```sh
 databricks configure --token
```

## Deploy python project and use in notebook


To deploy any python project *with a setup.py*

```sh
rocket trigger local_project_directory dbfs:/temp/your_folder
```

This command will return the exact command you have to perform in your notebook next:

Create a cell in the top of the notebook and paste the content (example below)

```sh
%pip install /dbfs/temp/your_folder/your-package0.0.1-py3-none-any.whl  --force-reinstall --no-deps
```

To keep tracking any file changes add the parameter `--enable-watch=True` to the trigger command.



Contributions are welcomed!

