figurepage
++++++++++

Create an HTML page to inspect a large number of figures at once.

Requires Python 3.6+.


Installation
============

Pip::

    pip install figurepage

Conda::

    conda install -c otaithleigh figurepage


Usage
=====

Given a directory structure like::

    .
    └── images
        ├── figure1.png
        └── figure2.png

Create a figure page for the files in ``images``::

    figurepage images

This creates a file ``figures.html`` in the current directory::

    .
    ├── figures.html
    └── images
        ├── figure1.png
        └── figure2.png
