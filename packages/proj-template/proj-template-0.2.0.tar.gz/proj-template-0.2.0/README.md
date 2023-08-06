proj-template
=============

`proj-template` is a CLI tool to generate a basic structure for Python
projects that use `setuptools` for build and distribution.


Installation
------------

Install through pip:

```
python3 -m pip install proj-template
```


Usage
-----

Create a [project description](config_example.yml) and execute:

```
proj_template <filename>
```

You may pipe the project description through the program:

```
cat <filename> | proj_template
```

