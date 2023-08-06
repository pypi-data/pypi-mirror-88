## PythonPackageSyncTool

PythonPackageSyncTool is a Python utility to "fix" requirements.txt.

It is used to make manipulation on requirements.txt that is produces by 'pip freeze'

### Getting Help

### QuickStart
First of all you should install alex_ber_utils (this dependency is used in setup.py). 

```bash
pip3 install -U alex_ber_utils
```

##
Than:


```bash
pip3 install -U python-package-sync-tool
```

##
```bash
cd /opt/anaconda3/lib/python3.7/site-packages/alexber/reqsync/data/
```
Note: This is Path where you're actually install my utility, it can be different in your machine.

If you use venv it will look something like:

```bash
cd /opt/MyProject/venv/Lib/site-packages/alexber/reqsync
```
##


Alternatively you can create sctipt file for yourself, named, say, driver.py:

```python3
#!/usr/bin/python3

import alexber.reqsync.app as app

if __name__ == "__main__":
   app.main()
```

Than create file config.yml near your script (see data/config.yml) or provide all parameter using command line
argruments. Use ':' in places where you should naturally write '==' (see explanation below).

Parammeters 'source' and 'destination' are required. You should also provide (requirements) file for 'source'.

`mutual_exclusion` has default value True.



##
Now, type

```bash
python3 -m alexber.reqsync.data --add=some_new_package:1.0.0
```

or if you're using script (driver.py) go the directory with the script and type
```bash
./driver.py --add=some_new_package:1.0.0
```

or if you install my tool to Anaconda/Python/venv that has it's bin folder is in the Path
you can run  
```bash
python_package_sync_tool --add=some_new_package:1.0.0
```

or alternativley

you can run  
```bash
reqsync --add=some_new_package:1.0.0
```


This will run quick check whether package is not in remove list. If it is, the utility will fail. You can override this
beahivor by supplying `--mutual_exclusion=False`. 

Then, this will add some_new_package with version 1.0.0 to the requirements-dest.txt

Note:

Semicolomn and not equal sign is used here due to Python limitaion of usage of equal sign in the value in the command line.

You can specified multiple packages using comma delimiter.

You can specifiy path to your config file using `--config_file`.

It can be absolute or relative. If you're running using script (driver.py), that it can be relative to the directory 
whether you put your script. If you're running as the module (`python3 -m`), it can be relative to 
`/opt/anaconda3/lib/python3.7/site-packages/alexber/reqsync/data/` (exact path can be different, see above).  

##
You can supplied multiply packages by using comma:


```bash
python3 -m alexber.reqsync.data --add=some_new_package:1.0.0,another_new_package:2.0.0
```
or if you're using script (driver.py) go the directory with the script and type
```bash
./driver.py --add=some_new_package:1.0.0,another_new_package:2.0.0
```


### Installing from Github

```bash
python3 -m pip install -U https://github.com/alex-ber/PythonPackageSyncTool/archive/master.zip
```
Optionally installing tests requirements.

```bash
python3 -m pip install -U https://github.com/alex-ber/PythonPackageSyncTool/archive/master.zip#egg=python-package-sync-tool[tests]
```

Or explicitly:

```bash
wget https://github.com/alex-ber/PythonPackageSyncTool/archive/master.zip -O master.zip; unzip master.zip; rm master.zip
```
And then installing from source (see below).



### Installing from source
```bash
python3 -m pip install . # only installs "required"
```
```bash
python3 -m pip install .[test] # installs dependencies for tests
```

### Using Docker
`alexberkovich/python_package_sync_tool:latest`  contains all `python_package_sync_tool` dependencies.
This Dockerfile is very simple, you can take relevant part for you and put them into your Dockerfile.

##
Alternatively, you can use it as base Docker image for your project and add/upgrade 
another dependencies as you need.

For example:

```Dockerfile
FROM alexberkovich/python_package_sync_tool:latest

COPY requirements.txt etc/requirements.txt

RUN set -ex && \
    #latest pip,setuptools,wheel
    pip install --upgrade pip setuptools wheel && \
    pip install python_package_sync_tool 
    pip install -r etc/requirements.txt 

CMD ["/bin/sh"]
#CMD tail -f /dev/null
```

where `requirements.txt` is requirements for your project.

##

From the directory with setup.py
```bash
python3 setup.py test #run all tests
```
```bash
pytest
```



## Requirements


PythonPackageSyncTool requires the following modules.

* Python 3.7+

* PyYAML==5.1

* alex-ber-utils==0.2.5
