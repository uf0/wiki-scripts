wiki-scripts
============

various script to get wikipedia data

##Installation
Install virtualenv:

``` sh
$ easy_install virtualenv
```

Download git repository:

``` sh
$ git clone https://github.com/uf0/wiki-scripts.git
```

browse to wiki-scripts root folder:

``` sh
$ cd wiki-scripts
```

Create a virtualenv directory `env`, activate the virtualenv and install the requirements:

``` sh
$ virtualenv --no-site-packages env
$ source env/bin/activate
$ pip install -r requirements.txt
```
##Run scripts

###usercontribs.py
This script gets in input a list of users and outputs the last 500 edits for each of them.

Type `$ python usercontribs.py -h` for usage instructions