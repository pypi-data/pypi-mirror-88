threedidepth
============

Calculate waterdepths for 3Di results.

* Interpolated or gridcell-constant waterlevels
* Interfaces with threediresults via `threedigrid`
* Progress indicator support
* Low memory consumption

For the interpolated mode, the 'lizard'-method is used. For a detailed
description, read the docstring for the `LizardLevelCalculator`.


Installation
------------

Make sure GDAL is available as (`from osgeo import gdal`)

$ pip install threedidepth


Usage
-----

From the cli::

    $ threedidepth gridadmin.h5 results_3di.nc dem.tif waterdepth.tif


Or python::

    >>> threedidepth.calculate_waterdepth(...)


Development installation with docker-compose
--------------------------------------------

For development, clone the repository and use a docker-compose setup::

    $ docker-compose build --build-arg uid=`id -u` --build-arg gid=`id -g` lib
    $ docker-compose up --no-start
    $ docker-compose start
    $ docker-compose exec lib bash

(Re)create & activate a virtualenv::

    (docker)$ rm -rf .venv
    (docker)$ virtualenv .venv --system-site-packages
    (docker)$ source .venv/bin/activate

Install dependencies & package and run tests::

    (docker)(virtualenv)$ pip install -r requirements.txt
    (docker)(virtualenv)$ pip install -e .[test]
    (docker)(virtualenv)$ pytest


Changelog of threedidepth
=========================


0.2 (2020-12-10)
----------------

- Implemented lizard method and set it as default.


0.1.2 (2020-09-21)
------------------

- Fix off-by-one-pixel nodgrid.


0.1.1 (2020-09-11)
------------------

- Fix flipped nodgrid.


0.1 (2020-09-03)
----------------

- First version.


