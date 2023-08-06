Welcome
=======

``high5py`` is a high-level interface to ``h5py``, which is itself a high-level interface to the HDF5 library.
You can use ``high5py`` to make one-line calls for the most common HDF5 tasks, like saving and loading data.
For example::

  import numpy as np
  import high5py as hi5

  hi5.save_dataset('data.h5', np.random.rand(100), name='x')
  x = hi5.load_dataset('data.h5', name='x')


Installation
============

The easiest way to install ``high5py`` is using pip::

  pip install high5py

To install from source, download the source code from Github::

  git clone git://github.com:jhtu/high5py.git

Next, navigate to the directory containing the source code, then build and install the package::

  python setup.py build
  python setup.py install

To be sure the code is working, run the unit tests::

  python -c 'import high5py as hi5; hi5.run_all_tests()'


Documentation
=============

The documentation is available at https://high5py.readthedocs.io.

You can also build the documentation manually with Sphinx
(http://sphinx.pocoo.org).
From the ``high5py`` directory, run ``sphinx-build docs docs/_build`` and then open
``docs/_build/index.html`` in a web browser.


Tutorial
========

A tutorial is provided as a Juptyer notebook (``tutorial.ipynb``), as well as in the online documentation at https://high5py.readthedocs.io.


Dependencies
============

``high5py`` requires ``numpy`` and ``h5py``.


Licensing
=========

``high5py`` is published under the BSD 3-clause license:

Copyright (c) 2012--2020, Jonathan Tu

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
