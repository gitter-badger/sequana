:Overview: Quality control, trimming (adapter removal) and taxonomic overview
:Input: A set of FastQ (paired or single-end)
:Output: fastqc, cleanup FastQ files

Usage
~~~~~~~

::

    sequana --pipeline quality_control --input-directory . --output-directory analysis


Requirements
~~~~~~~~~~~~~~~~~~

.. include:: ../sequana/pipelines/quality_control/requirements.txt

.. image:: https://raw.githubusercontent.com/sequana/sequana/master/sequana/pipelines/quality_control/dag.png


Details
~~~~~~~~~


The adapters are removed using cutadapt. If one specifies 
the quality trimming option in the config file, then we trim
low-quality ends from reads BEFORE adapter removal.

The quality trimming algorithm is the same as in BWA. That is: substract the
cutoff (e.g. 30) from all qualities; compute partial sums from the end of the
sequence; cut the sequence at the index at which the sum is minimal.

::

    # Original qualities
    42, 40, 26, 27, 8, 7, 11, 4, 2, 3
    # Subtracting the threshold gives:
    32, 30, 16, 17, -2, -3, 1, -6, -8, -7
    # Partial sum from the end. Stop early if the sum is greater than zero:
    (70), (38), 8, -8, -25, -23, -20, -21, -15, -7

Minimum is -25, we keep the bases 1,2,3,4::

    42, 40, 26, 27

Another important point is that all searches for adapter 
sequences are error tolerant (allowing errors such as 
mismatches, insertions and deletions). The level of error tolerance
is 10% by default.

Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is a documented configuration file :download:`../sequana/pipelines/quality_control/config.yaml` to be used with the pipeline. Each rule used in the pipeline may have a section in the
configuration file. Here are the rules and their developer and user documentation.



FastQC
^^^^^^^^^^^
.. snakemakerule:: fastqc

Cutadapt
^^^^^^^^^
.. snakemakerule:: cutadapt

Kraken
^^^^^^^
.. snakemakerule:: kraken


.. .. snakemakerule:: fastq_sampling
.. .. snakemakerule:: bwa_mem_phix







