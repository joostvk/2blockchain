# Introduction 

This repo contains instructions for setting-up and using:

- Azure functions
- Alert database
- Azure DataFactory

## Azure functions

### Seting up 

- https://michael-mckenna.com/how-to-import-python-extension-modules-in-azure-functions/
- http://www.lfd.uci.edu/~gohlke/pythonlibs

In Kudu perform the following steps to setup a virtual env and install python packages:

1. Make sure the wheel of the package you want to install is located in the wheelhouse directory (check if filename is ok e.g. cp27m should be replace with none). Also, add wheels of all dependencies.
2. Add package to requirements.txt
3. Go to wwroot dir: `cd D:\home\site\wwwroot`
4. Create virtual env: `D:\python27\scripts\virtualenv env`
5. Activate virtal env: `env\Scripts\activate`
6. Install packages: `pip install -r requirements.txt`

Now add the following line to your python code to enable the installed packages:
`sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'env/Lib/site-packages')))`

### End points

\\TODO

## Initialize DB

\\TODO

## Data factory

- https://docs.microsoft.com/en-gb/azure/data-factory/data-factory-stored-proc-activity

\\TODO"# 2blockchain" 
