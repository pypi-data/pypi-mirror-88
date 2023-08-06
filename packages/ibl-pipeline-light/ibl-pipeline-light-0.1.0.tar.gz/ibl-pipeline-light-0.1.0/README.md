# IBL-pipeline-light
A light version of IBL pipeline that allows users to access datajoint tables.



## Modules
A user connecting to the public IBL database could use the following modules:

`reference`, `subject`, `action`, `acquisition`, `data`, `behavior`, and `analyses.behavior`.

In addition to the above modules, an IBL internal user connecting to the internal IBL database could use the following modules as well:

`ephys`, `histology`, `qc`


## Install package and set up the configuration

The package is released on PyPI and could be installed with the following command:

```bash
pip install ibl-pipeline-light
```

To connect to the database for the first time, you will need to set up the DataJoint config within python.

```python
import datajoint as dj
dj.config['database.host'] = {host_name}
dj.config['database.user'] = {user_name}
dj.config['database.password'] = {password}
dj.config.save_local()
```
`host_name` is either the IBL public database `datajoint-public.internationalbrainlab.org` or the internal database `datajoint.internationalbrainlab.org`.

`dj.config.save_local()` saves the config file in the local directory, which allows direct connection to the database in this directory.

If you need the global config that allows direct connection from any directory, use `dj.config.save_global()` instead.

After these, you will be able to import the modules:

```python
from ibl_pipeline import reference, subject, action, acquisition, behavior
```
