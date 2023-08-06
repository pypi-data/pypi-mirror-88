# demo-pip-sample

# Upload

```
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
    Output
    Enter your username: rich_python
    Enter your password: 
    Uploading example1_pkg_rich-0.0.1-py3-none-any.whl
    100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 17.2k/17.2k [00:01<00:00, 9.20kB/s]
    Uploading example1-pkg-rich-0.0.1.tar.gz
    100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4.76k/4.76k [00:00<00:00, 5.82kB/s]

    View at:
    https://pypi.org/project/example1-pkg-rich/0.0.1/
```

# install
```
pip3 install example1-pkg-rich
```

# call
```
python3     # terminal
OTHER_SECRET="test-secret"

# Client
export OTHER_SECRET="test-secret"

from clientTest import utils
utils.utilsFechaOfClient()
```

# tree

├── LICENSE
├── README.md
├── build
│   ├── bdist.macosx-10.13-x86_64
│   └── lib
│       └── clientTest
│           ├── __init__.py
│           ├── __main__.py
│           └── utils.py
├── clientTest
│   ├── __init__.py
│   ├── __main__.py
│   ├── config.cfg
│   └── utils.py
├── dist
│   ├── example1-pkg-rich-0.0.1.tar.gz
│   └── example1_pkg_rich-0.0.1-py3-none-any.whl
├── example1_pkg_rich.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   └── top_level.txt
└── setup.py