# demo-pip-sample

# Upload

```
python3 setup.py sdist bdist_wheel
python -m twine upload dist/*
```

# install
```
pip3 install example1-pkg-rich
```

# call
>>> from clientTest import utils
>>> utils.utilsFechaOfClient()