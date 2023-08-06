# EDD Utils
This package is a utility for downloading **Experiment Data Depot** study instances through python or the commandline. It was coded and is to be used in Python 3.6+. The package can be installed on your system through pip via the command

```console
pip install edd-utils
```

The package has two entry points, either as a commandline utility or as a python module. The commandline utility is used as below:

```console
$ export_edd_study my_edd_study_slug --username my_edd_username --server my.edd.server.org
```

For an example of how to use the python module see the jupyter notebook in the notebooks directory.

Note: The progressbar functionality will run correctly on JupyterLab v0.35.6 with enabled jupyterlab-manager labextension, which can be installed by

```console
 jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

Login credentials can also be provided in a configuration file, `~/.eddrc`:
```
[edd.server1.org]
username: my_user_name1
password: my_password1

[edd.server2.org]
username: my_user_name2
password: my_password2
```

## License

`edd-utils` is available under the [BSD-3-Clause-LBNL license](https://github.com/JBEI/edd-utils/blob/master/LICENSE.txt).
