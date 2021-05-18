![image](https://user-images.githubusercontent.com/2252355/118677158-5293ed80-b7fc-11eb-9619-e98829bbc9ce.png)

Keep your local python scripts installed and in sync with a databricks notebook.
Shortens the feedback loop to develop projects using a hybrid enviroment.
Every change on your local machine is directly applied to the notebook.


## Installing


```sh
pip install databricks-rocket
```


For the library to work you need databricks-cli configured with a valid token.
If you haven't done so yet just run:

```sh
pip install databricks-cli
databricks configure --token
#optionally run the following to make sure your configuration is ok
databricks-connect test
```

## Deploy python project and use in notebook


To deploy any python project *with a setup.py*

```sh
rocket trigger local_project_directory dbfs:/your_temp_folder
# /your_temp_folder can be any path in dbfs you have permission
# if the directory is not there it will be created
```


This command will return the exact command you have to perform in your notebook next:

Create a cell in the top of the notebook and paste the content (example below)

```sh
%pip install /dbfs/temp/your_folder/your-package0.0.1-py3-none-any.whl  --force-reinstall --no-deps
```

To keep tracking any file changes add the parameter `--enable-watch=True` to the trigger command.

## Troubleshooting

If building your package is failing upgrade the build library:

```sh
python3 -m pip install --upgrade build 
```



## Acknowledgments

- Thanks Leon Poli for the Logo :)
- Stephane Leonard for source-code and documentation improvements :)

Contributions are welcomed!
