[![pipeline status](https://gitlab.com/remytms/prgconfig/badges/master/pipeline.svg)](https://gitlab.com/remytms/prgconfig/pipelines)
[![coverage report](https://gitlab.com/remytms/prgconfig/badges/master/coverage.svg)](https://gitlab.com/remytms/prgconfig/pipelines)
[![licence](https://img.shields.io/pypi/l/prgconfig.svg)](https://www.gnu.org/licenses/gpl.html)
[![version](https://img.shields.io/pypi/v/prgconfig.svg)](https://pypi.org/project/prgconfig)
[![python](https://img.shields.io/pypi/pyversions/prgconfig.svg)](https://pypi.org/project/prgconfig)

prgconfig
=========

prgconfig is a little library that ease the manage of configuration
file written in [toml](https://toml.io). It comes with nice default. The
minimum you have to specify is your program name then it does the rest.
It aims to fit to standard in use for location of configuration file. It
is also totally configurable to fit your needs.


Installation
------------

Recommended installation is by using `pip`:

```sh
pip install prgconfig
```


Usage
-----

`PrgConfig` is a dict like object.

Basic example:

```python
from prgconfig import PrgConfig

config = PrgConfig("prgname")

config.load()

print(config["section"]["key"])
```

See the constructor of `PrgConfig` class to get an idea of possible
configuration.


Roadmap
-------

See [issues with the `enhancement` tag](https://gitlab.com/remytms/prgconfig/-/issues?scope=all&utf8=%E2%9C%93&state=opened&label_name[]=enhancement)
