## vmdatastore: vCenter datastore manager 

This command-line tool lets you add datastores to your ESX hosts.

Requirements
* linux or windows box
* Python 2.6 or higher
* [argparse](https://docs.python.org/3/library/argparse.html) library
* [pyvmomi](https://github.com/vmware/pyvmomi) library
* access to a VMWare vCenter host

Installation:
-------------
* Clone repository   
`git clone https://github.com/sebbrochet/vmdatastore.git`
* cd into project directory   
`cd vmdatastore`
* Install requirements with pip   
`pip install -r requirements.txt`
* Install vmdatastore binary   
`python setup.py install`

Usage:
------

```
usage: vmdatastore [-h] [-u USER] [-p PASSWORD] [-t TARGET] [-o PORT]
                   [-c CONFIG] [-v]
                   command

vCenter datastore manager.

positional arguments:
  command               Command to execute (list_datastore,
                        list_unresolved_volumes, resignature_volumes,
                        resolve_volumes)

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  Specify the user account to use to connect to vCenter
  -p PASSWORD, --password PASSWORD
                        Specify the password associated with the user account
  -t TARGET, --target TARGET
                        Specify the vCenter host to connect to
  -o PORT, --port PORT  Port to connect on (default is 443)
  -c CONFIG, --config CONFIG
                        Configuration file to use
  -v, --version         Print program version and exit.
```
