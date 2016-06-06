Sequana documentation
##########################################

|version|, |today|


.. image:: https://badge.fury.io/py/sequana.svg
    :target: https://pypi.python.org/pypi/sequana

.. image:: https://travis-ci.org/sequana/sequana.svg?branch=master
    :target: https://travis-ci.org/sequana/sequana

.. image::  https://coveralls.io/repos/github/sequana/sequana/badge.svg?branch=master
   :target: https://coveralls.io/github/sequana/sequana?branch=master 

.. image:: http://readthedocs.org/projects/sequana/badge/?version=master
    :target: http://sequana.readthedocs.org/en/latest/?badge=master
    :alt: Documentation Status


:Python version: Python 2.7 and 3.5
:Issues and bug reports: `On github <https://github.com/sequana/sequana/issues>`_


What is Sequana ?
=====================

Sequana provides (i) modules and pipelines dedicated to NGS in the form of Snakefiles (Makefile-like syntax with Python syntax) and (ii) tools to help in the creation of such pipelines (iii) original data analysis or data handling tools dedicated to NGS and (iv) set of HTML reports.

Sequana can be used by developers to create new pipelines and by users in the
form of applications ready for production.


Installation
#################


:: 

    pip install sequana

With conda::

    conda install numpy pandas matplotlib
    pip install sequana

Examples
##########

Given a set of FASTQ files in a local directory, you can run a pipeline as
follows (given its name)::

    sequana --init quality
    # EDIT the file config.yaml to provide the fastq files
    # and the project name (e.g. TEST)
    
Run the pipelines and wait for completion. Check the output ::
    
    # Note that in version 0.1.4, you must rename the Snakefile into **Snakefile**
    
    snakemake -s Snakefile --stats stats.txt -p -j 4
    
And finally, open the report in ./TEST::

    open TEST/report_quality.html



This will copy the Snakefile locally as well as the corresponding configuration
file.

Pipelines can be found in the directory ./pipelines or ./rules



Issues
##########

Please fill bug report in https://github.com/sequana/sequana



.. toctree::
    :numbered: 
    :maxdepth: 2

    userguide
    pipelines
    auto_examples/index
    references
    faqs
    Changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`