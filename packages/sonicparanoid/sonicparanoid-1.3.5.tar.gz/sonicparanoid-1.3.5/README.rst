|  |downloads| |version| |py-versions| |license|

.. |downloads| image:: https://img.shields.io/pypi/dm/sonicparanoid.svg
    :target: https://pepy.tech/project/sonicparanoid
    :alt: Downloads

.. |version| image:: https://img.shields.io/pypi/v/sonicparanoid.svg?label=latest%20version
    :target: https://pypi.org/project/sonicparanoid
    :alt: Latest version

.. |py-versions| image:: https://img.shields.io/pypi/pyversions/sonicparanoid.svg
    :target: https://pypi.org/project/sonicparanoid
    :alt: Supported Python versions

.. |license| image:: https://img.shields.io/pypi/l/sonicparanoid.svg?color=green
    :alt: License

-----

SonicParanoid
=============

A fast, accurate and easy to use orthology inference tool.

Description
===========

SonicParanoid is a stand-alone software for the identification of orthologous relationships among multiple species. SonicParanoid is an open source software released under the GNU GENERAL PUBLIC LICENSE, Version 3.0 (GPLv3), implemented in Python3, Cython, and C++. It works on Linux and Mac OSX. The software is designed to run using multiple processors and proved to be up to 1245X faster then InParanoid, 166X faster than Proteinortho, and 172X faster than OrthoFinder 2.0 with an accuracy comparable to that of well-established orthology inference tools.
Thanks to its speed, accuracy, and usability SonicParanoid substantially relieves the difficulties of orthology inference for biologists who need to construct and maintain their own genomic datasets.

SonicParanoid was tested on the 2011 version of a benchmark proteome dataset provided by the Quest for Orthologs (QfO) consortium (https://questfororthologs.org), and its accuracy was assessed, and compared to that of other 13 methods, using a publicly available orthology benchmarking service (http://orthology.benchmarkservice.org).

SonicParanoid is available at http://iwasakilab.bs.s.u-tokyo.ac.jp/sonicparanoid.

Citation
===========

> Salvatore Cosentino and Wataru Iwasaki (2018) SonicParanoid: fast, accurate and easy orthology inference. Bioinformatics

> Volume 35, Issue 1, 1 January 2019, Pages 149–151,

> https://doi.org/10.1093/bioinformatics/bty631

Changelog
===========
1.3.3 (July 25, 2020)
 - Enhancement: execution is 5~10% faster when many small proteomes are given input (e.g. > 1000)
 - Enhancement: considerably reduced IO when generating the alignments
 - Enhancement: more informative output from the command line
 - Enhancement: output directories are now easier to browse even when many input files are provided
 - Enhancement: MCL binaries automatically installed for Linux and MacOS
 - Enhancement: warnings are shown only in debug mode
 - Enhancement: avoid users to restart a run using a different MMseqs sensitivity
 - Enhancement: automatically remove incomplete alignments when restarting a run
 - Maintanance: added `wheel` as a dependency and removed `sh`
 - Maintenance: upgraded to `MMseqs2 version 11-e1a1c <https://github.com/soedinglab/MMseqs2/releases/tag/11-e1a1c>`_
 - Fix: `Inconsistent results when using non-indexed target databases <https://gitlab.com/salvo981/sonicparanoid2/-/issues/18>`_. Big thanks to `Keito <https://twitter.com/watano_k10>`_ for providing the dataset.
 - Fix: `wrongly formatted execution times <https://gitlab.com/salvo981/sonicparanoid2/-/issues/19>`_ in the alignments stats file.
 - Breaking change: alignments and ortholog tables are now organized into subdirectories, please check the `web-page <http://iwasakilab.bs.s.u-tokyo.ac.jp/sonicparanoid/>`_ for details

1.3.2 (April 23, 2020)
 - Enhancement: Added support for Python 3.8
 - Maintanance: Increased minimum version for packages, Cython(0.29); pandas(1.0); numpy(1.18); scikit-learn(0.22); scipy(1.2.1); mypy(0.720); biopython(1.73)
 - Maintenance: Retrained prediction models using the latest version scikit-learn (0.22)
 - Fix: `Too many open files error <https://gitlab.com/salvo981/sonicparanoid2/-/issues/15>`_. Big thanks to `Eva Deutekom <https://twitter.com/EvanderDeut>`_
 - Fix: `Removed scikit-lean warnings <https://gitlab.com/salvo981/sonicparanoid2/-/issues/10>`_.

1.3.0 (November 26, 2019)
 - Enhancement: SonicParanoid is much faster when using high sensitivity modes! Check the `web-page <http://iwasakilab.bs.s.u-tokyo.ac.jp/sonicparanoid/#extimes>`__...
 - Enhancement: run directory names embed information about the run settings
 - Enhancement: generated temporary files are much smaller now
 - Fix: `error with only 2 input species <https://gitlab.com/salvo981/sonicparanoid2/issues/9>`_. Big thanks to `Benjamin Hume <https://scholar.google.co.jp/citations?hl=en&user=gZj6l8sAAAAJ>`_
 - Fix: force overwriting of MMseqs2 binaries if the version is different from the supported one
 - Usability: Tested on Arch-based `Manjaro Linux <https://manjaro.org>`_
 - Others: Big thanks to `Shun Yamanouchi <https://twitter.com/Mt_Nuc>`_ for providing some challenging datasets used for testing
 - Maintenance: upgraded to `MMseqs2 version 10-6d92c <https://github.com/soedinglab/MMseqs2/releases/tag/10-6d92c>`_

1.2.6 (August 26, 2019)
 - Fix: ``"to many files open"`` error which sometimes happened when using more than 20 threads

1.2.5 (August 7, 2019)
 - Fix: Logical threads are considered instead of physical cores in the adjustment of the threads number
 - Requirements: a minimum of 1.75 gigabytes per thread is required (the number of threads is automatically adjusted)
 - Enhancement: added parameter ``--force-all-threads`` to bypass the check for minimum per-thread memory

1.2.4 (July 14, 2019)
 - Enhancement: Added control to avoid selecting a number threads higher than the available physical CPU cores (big thanks to `Shun Yamanouchi <https://twitter.com/Mt_Nuc>`__)
 - Fix: Removed some scipy warnings, now shown only in debug mode (thanks to `Alexie Papanicolaou <https://gitlab.com/alpapan>`_)
 - Requirements: `psutils <https://pypi.org/project/psutil/>`_>=5.6.0 is now required
 - Requirements: `mypy <https://pypi.org/project/mypy/>`_>=0.701 is now required
 - Requirements: at least Python 3.6 is now required

1.2.3 (June 7, 2019)
 - Enhancement: some error messages are more informative (big thanks to `Jeff Stein <https://gitlab.com/jvstein>`_)

1.2.2 (May 13, 2019)
 - Fix: solved a bug that caused MCL to be not properly compiled on some Linux distributions
 - Info: source code migrated to `GitLab <https://gitlab.com/salvo981/sonicparanoid2>`_

1.2.1 (May 10, 2019)
 - Fix: solved bug related to random missing alignments
 - Info: this issue was first described in `here <https://bitbucket.org/salvocos/sonicparanoid/issues/2/two-problems-with-qfo2011>`_

1.2.0 (April 26, 2019)
 - Change: Markov Clustering (MCL) is now used by default for the creation of ortholog groups
 - Enhancement: the MCL inflation can be controlled through the parameter ``--inflation``
 - Enhancement: Output file with single-copy ortholog groups
 - Feature: single-linkage clustering for ortholog groups creation through the ``--single-linkage`` parameter
 - Enhancement: added secondary program to filter ortholog groups
 - Info: type ``sonicparanoid-extract --help`` to see the list of options
 - Enhancement: Filter ortholog groups by species ID
 - Enhancement: Filter ortholog groups by species composition (e.g., only groups with given number of species)
 - Enhancement: Extract FASTA sequences of orthologs in selected groups
 - Fix: The correct version of SonicParanoid is now shown in the help
 - Others: General bug fixes and under-the-hood improvements

1.1.2 (March, 2019)
 - Enhancement: Filter ortholog groups by species ID
 - Enhancement: Filter ortholog groups by species composition (e.g., only groups with given number of species)
 - Enhancement: Extract FASTA files corresponding orthologs in selected groups
 - Fix: The correct version of SonicParanoid is now shown in the help

1.1.1 (January 24, 2019)
 - Enhancement: No restriction on file names
 - Enhancement: No restriction on symbols used in FASTA headers
 - Enhancement: Added file with genes that could not be inserted in any group (not orthologs)
 - Enhancement: Added some statistics on the predicted ortholog groups
 - Enhancement: Update runs are automatically detected
 - Enhancement: Improved inference of in-paralogs
 - Change: The directory structure has been redesigned to better support run updated

1.0.14 (October 19, 2018)
 - Enhancement: a warning is shown if non-protein sequences are given in input
 - Enhancement: upgraded to MMseqs2 6-f5a1c
 - Enhancement: SonicParanoid is now available through Bioconda (https://bioconda.github.io/recipes/sonicparanoid/README.html)

1.0.13 (September 18, 2018)
 - Fix: allow FASTA headers containing the '@' symbol

1.0.12 (September 7, 2018)
 - Improved accuracy
 - Added new sensitivity mode (most-sensitive)
 - Fix: internal input directory is wiped at every new run
 - Fix: available disk space calculation

1.0.11 (August 7, 2018)
 - Added new program (sonicparanoid-extract) to process output multi-species clusters
 - Added the possibility to analyse only 2 proteomes
 - Added support for Python3.7
 - Python3 versions: 3.5, 3.6, 3.7
 - Upgraded MMseqs2 (commit: a856ce, August 6, 2018)

1.0.9 (May 10, 2018)
 - First public release
 - Python3 versions: 3.4, 3.5, 3.6
