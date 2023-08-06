.. _installation:

============
Installation
============


Using Anaconda or Miniconda (recommended)
-----------------------------------------

Using conda_ (latest version recommended), sensormapgeo is installed as follows:


1. Create virtual environment for sensormapgeo (optional but recommended):

   .. code-block:: bash

    $ conda create -c conda-forge --name sensormapgeo python=3
    $ conda activate sensormapgeo


2. Then install sensormapgeo itself:

   .. code-block:: bash

    $ conda install -c conda-forge sensormapgeo


This is the preferred method to install sensormapgeo, as it always installs the most recent stable release and
automatically resolves all the dependencies.


Using pip (not recommended)
---------------------------

There is also a `pip`_ installer for sensormapgeo. However, please note that sensormapgeo depends on some
open source packages that may cause problems when installed with pip. Therefore, we strongly recommend
to resolve the following dependencies before the pip installer is run:


    * _openmp_mutex=*=*llvm*
    * geopandas
    * gdal
    * lxml
    * numpy
    * pyproj
    * pyqt
    * pyresample
    * scikit-image


Then, the pip installer can be run by:

   .. code-block:: bash

    $ pip install sensormapgeo

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.



.. note::

    sensormapgeo has been tested with Python 3.6+.,
    i.e., should be fully compatible to all Python versions from 3.6 onwards.


.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _conda: https://conda.io/docs
