# GTDB Validation Toolkit

[![version status](https://img.shields.io/pypi/v/gtdb_validation_tk.svg)](https://pypi.python.org/pypi/gtdb_validation_tk)
[![ace-internal](https://img.shields.io/conda/vn/ace-internal/gtdb_validation_tk.svg?color=green)](https://anaconda.org/ace-internal/gtdb_validation_tk)
[![Downloads](https://pepy.tech/badge/gtdb_validation_tk)](https://pepy.tech/project/gtdb_validation_tk)
[![Downloads](https://pepy.tech/badge/gtdb_validation_tk/month)](https://pepy.tech/project/gtdb_validation_tk/month)

This toolkit provides functionality for validation the GTDB Taxonomy. It is primarily intended to be used by the GTDB curation team, but has been made available in case others find it useful. 

## Install

The simplest way to install this package is through pip:
> sudo pip install gtdb_validation_tk

## Package updates

#### PyPI
```shell script
python3 setup.py sdist wheel
python3 -m twine upload dist/*
```

#### Anaconda
1. Clone the https://github.com/Ecogenomics/ace-conda repository on a CentOS server.
2. Create a new `meta.yaml`, [similar to previous versions](https://github.com/Ecogenomics/ace-conda/tree/master/pkg/gtdb_validation_tk) (adding any new dependencies) 
3. Build and upload the package according to the instructions in [ace-conda](https://github.com/Ecogenomics/ace-conda).
4. Update the server modulefiles according to the [ACE wiki](https://wiki.ecogenomic.org/doku.php?id=managing_modulefiles_conda_environments)

## Cite

If you find this package useful, please cite this git repository (https://github.com/Ecogenomics/gtdb_validation_tk)

## Copyright

Copyright © 2019 Donovan Parks. See LICENSE for further details.
