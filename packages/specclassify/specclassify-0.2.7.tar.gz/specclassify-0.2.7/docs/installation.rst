.. _installation:

============
Installation
============


Using Anaconda or Miniconda (recommended)
-----------------------------------------

Using conda_ (latest version recommended), specclassify is installed as follows:


1. Create virtual environment for specclassify (optional but recommended):

   .. code-block:: bash

    $ conda create -c conda-forge --name specclassify python=3
    $ conda activate specclassify


2. Then install specclassify itself:

   .. code-block:: bash

    $ conda install -c conda-forge specclassify


This is the preferred method to install specclassify, as it always installs the most recent stable release and
automatically resolves all the dependencies.


Using pip (not recommended)
---------------------------

There is also a `pip`_ installer for specclassify. However, please note that specclassify depends on some
open source packages that may cause problems when installed with pip. Therefore, we strongly recommend
to resolve the following dependencies before the pip installer is run:


    * gdal
    * geopandas
    * matplotlib
    * numpy
    * pyproj >=2.1.0
    * scikit-image
    * scikit-learn
    * shapely


Then, the pip installer can be run by:

   .. code-block:: bash

    $ pip install specclassify

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.



.. note::

    specclassify has been tested with Python 3.6+.,
    i.e., should be fully compatible to all Python versions from 3.6 onwards.


.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _conda: https://conda.io/docs
