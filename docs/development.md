# Developing on local machine

## 1. Clone the repo

Find the right branch.

## 2. Install local db rocket in dev. mode


```sh
cd dbrocket_folder
pip install -e . 

```

From here one rocket should be the dev one.

## Build the package and upload it to PyPi

One needs to get pypi crendentials to upload. Reach out in case of need.

```sh
pip install twine
./release.py release
```
