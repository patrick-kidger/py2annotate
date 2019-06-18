***********
py2annotate
***********
An extension to Sphinx `autodoc` to augment sphinx documentation with type annotations, when using Python 2 style type annotations.

The Problem
===========
Python 2 doesn't support type annotations. Thus writing Python 2 / Python 3 agnostic code with type annotations requires `putting the type annotations in comments <https://mypy.readthedocs.io/en/latest/python2.html>`__:

.. code-block:: python

    def add(x, y):
        # type: (int, int) -> int
        """Adds two numbers."""
        return x + y

But now when documentation is generated with `sphinx <http://www.sphinx-doc.org/en/master/>`__, the documentation doesn't include type annotations:

.. image:: https://raw.githubusercontent.com/patrick-kidger/py2annotate/master/imgs/without-annotations.png
    :align: center


*Example from the* |signatory|_ *project.*

.. _signatory: https://github.com/patrick-kidger/signatory
.. |signatory| replace:: *Signatory*

The Solution
============

This extension remedies things so that the Sphinx documentation now looks like:

.. image:: https://raw.githubusercontent.com/patrick-kidger/py2annotate/master/imgs/with-annotations.png
    :align: center

.. role:: python(code)
    :language: python

(which is the same as what you'd get using Python 3 style type annotations e.g. :python:`def add(x: int, y: int) -> int`)

Installation
============
Via pip:

.. code-block:: bash

    pip install py2annotate

It's also just a single file, so copy-paste the code if you want.

Usage
=====
Just add py2annotate to the list of extensions in `conf.py`:

.. code-block:: python

    # conf.py
    ...
    extensions = ['sphinx.ext.autodoc', 'py2annotate']
    ...

(It shouldn't matter whether it comes before or after `autodoc`.)

Note that Sphinx itself must be run using Python 3, not Python 2. This is because `py2annotate` uses the Python 3 style
type annotations internally in order to determine the correct annotations.

Known Issues
============
None so far! File a report if you run into anything. `mypy <https://mypy.readthedocs.io/en/latest/index.html>`__ and `stubgen <https://mypy.readthedocs.io/en/latest/stubgen.html>`__ are used internally though, so your code's formatting must be in a manner that they understand.