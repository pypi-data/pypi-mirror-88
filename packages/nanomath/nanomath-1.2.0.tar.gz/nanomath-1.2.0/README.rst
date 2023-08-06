nanomath
========

This module provides a few simple math and statistics functions for
other scripts processing Oxford Nanopore sequencing data

|Twitter URL| |install with conda| |install with Debian| |Build Status|
|Code Health|

FUNCTIONS
---------

-  Calculate read N50 from a set of lengths ``get_N50(readlenghts)``
-  Remove extreme length outliers from a dataset
   ``remove_length_outliers(dataframe, columname)``
-  Calculate the average Phred quality of a read
   ``ave_qual(qualscores)``
-  Write out the statistics report after calling readstats function
   ``write_stats(dataframe, outputname)``
-  Compute a number of statistics, return a dictionary
   ``calc_read_stats(dataframe)``

INSTALLATION
------------

.. code:: bash

   pip install nanomath

| or
| |install with conda|

::

   conda install -c bioconda nanomath

STATUS
------

|Build Status|

CONTRIBUTORS
------------

[@alexomics](https://github.com/alexomics) for fixing the indentation of
the printed stats

CITATION
--------

If you use this tool, please consider citing our
`publication <https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/bty149/4934939>`__.

.. |Twitter URL| image:: https://img.shields.io/twitter/url/https/twitter.com/wouter_decoster.svg?style=social&label=Follow%20%40wouter_decoster
   :target: https://twitter.com/wouter_decoster
.. |install with conda| image:: https://anaconda.org/bioconda/nanomath/badges/installer/conda.svg
   :target: https://anaconda.org/bioconda/nanomath
.. |install with Debian| image:: https://www.debian.org/logos/button-mini.png
   :target: https://tracker.debian.org/pkg/python-nanomath
.. |Build Status| image:: https://travis-ci.org/wdecoster/nanomath.svg?branch=master
   :target: https://travis-ci.org/wdecoster/nanomath
.. |Code Health| image:: https://landscape.io/github/wdecoster/nanomath/master/landscape.svg?style=flat
   :target: https://landscape.io/github/wdecoster/nanomath/master
