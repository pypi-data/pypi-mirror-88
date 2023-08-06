# Flask-Restless-NG #

[![PyPI version](https://badge.fury.io/py/Flask-Restless-NG.svg)](https://badge.fury.io/py/Flask-Restless-NG)
[![Build Status](https://travis-ci.org/mrevutskyi/flask-restless-ng.svg?branch=master)](https://travis-ci.org/mrevutskyi/flask-restless-ng)
[![Coverage Status](https://coveralls.io/repos/github/mrevutskyi/flask-restless-ng/badge.svg?branch=master)](https://coveralls.io/github/mrevutskyi/flask-restless-ng?branch=master)

## About

This is a fork of [Flask-Restless](https://github.com/jfinkels/flask-restless) module originally written by Jeffrey Finkelstein.
Flask-Restless is a great tool to build [JSON API][2] for SQLAlchemy models, but unfortunately is
no longer maintained and does not support the most recent versions of Flask and SQLAlchemy 

Version `1.0.*` of `Flask-Restless-NG` is fully API compatible with `Flask-Restless` version `1.0.0b1`
with the following improvements:

  * Supports Flask 1.0+ and SQLAlchemy 1.3+
  * 2-5x faster serialization of JSON responses.
  * Miscellaneous bugs fixed

## Introduction ##

This is Flask-Restless, a [Flask][1] extension that creates URL endpoints that
satisfy the requirements of the [JSON API][2] specification. It is compatible
with models that have been defined using either [SQLAlchemy][3] or
[Flask-SQLAlchemy][4].

This document contains some brief instructions concerning installation of
requirements, installation of this extension, configuration and usage of this
extension, and building of documentation.

For more information, see the

  * [documentation][5],
  * [Python Package Index listing][6],
  * [source code repository][7].

[1]: http://flask.pocoo.org
[2]: https://jsonapi.org
[3]: https://sqlalchemy.org
[4]: https://packages.python.org/Flask-SQLAlchemy
[5]: https://flask-restless-ng.readthedocs.org
[6]: https://pypi.python.org/pypi/Flask-Restless-NG
[7]: https://github.com/mrevutskyi/flask-restless-ng

## Copyright license ##

The code comprising this program is copyright 2011 Lincoln de Sousa and
copyright 2012, 2013, 2014, 2015, 2016 Jeffrey Finkelstein and contributors,
and is dual-licensed under the following two copyright licenses:

* the GNU Affero General Public License, either version 3 or (at your option)
  any later version
* the 3-clause BSD License

For more information, see the files `LICENSE.AGPL` and `LICENSE.BSD` in this
directory.

The documentation is licensed under the Creative Commons Attribution-ShareAlike
4.0 license.

## Contents ##

This is a partial listing of the contents of this package.

* `LICENSE.AGPL` - one possible copyright license under which this program is
  distributed to you (the GNU Affero General Public License version 3)
* `LICENSE.BSD` - another possible copyright license under which this program
  is distributed to you (the 3-clause BSD License)
* `docs/` - the Sphinx documentation for Flask-Restless
* `examples/` - example applications of Flask-Restless
* `flask_restless/` - the Python package containing the extension
* `MANIFEST.in` - indicates files to include when packaging Flask-Restless
* `README.md` - this file
* `setup.py` - Python setuptools configuration file for packaging this
  extension
* `tests/` - unit tests for Flask-Restless

The `flask_restless` directory is a Python package containing the following
files and directory:

* `helpers.py` - utility functions, mainly for performing introspection on
  SQLAlchemy objects
* `manager.py` - contains the main class that end users will utilize to create
  ReSTful JSON APIs for their database models
* `search.py` - functions and classes that facilitate searching the database
  on requests that require a search
* `serialization.py` - basic serialization and deserialization for SQLAlchemy
  models
* `views/` - the view classes that implement the JSON API interface

## Installing

This application can be used with any Python version 3.6+ 

This application requires the following libraries to be installed:

* [Flask][1] version 1.0 or greater
* [SQLAlchemy][3] version 1.2 or greater
* [python-dateutil][8] version strictly greater than 2.2
* [mimerender][9] version 0.5.2 or greater

These requirements (and some additional optional packages) are also listed in
the `requirements.txt` file. Using `pip` is probably the easiest way to install
these:

    pip install -r requirements.txt

[8]: https://labix.org/python-dateutil
[9]: https://github.com/martinblech/mimerender

## Building as a Python egg ##

This package can be built, installed, etc. as a Python egg using the provided
`setup.py` script. For more information, run

    python setup.py --help

## How to use ##

For information on how to use this extension, build the documentation here or
[view it on the Web][5].

## Testing ##

Using `pip` is probably the easiest way to install this:

    pip install -r requirements-test.txt

To run the tests:

    python -m unittest


## Building documentation ##

Flask-Restless requires the following program and supporting library to build
the documentation:

* [Sphinx][11]
* [sphinxcontrib-httpdomain][12], version 1.1.7 or greater

These requirements are also listed in the `requirements-doc.txt` file. Using
`pip` is probably the easiest way to install these:

    pip install -r requirements-doc.txt

The documentation is written for Sphinx in [reStructuredText][13] files in the
`docs/` directory. Documentation for each class and function is provided in the
docstring in the code.

The documentation uses the Flask Sphinx theme. It is included as a git
submodule of this project, rooted at `docs/_themes`. To get the themes, do

    git submodule update --init

Now to build the documentation, run the command

    python setup.py build_sphinx

in the top-level directory. The output can be viewed in a web browser by
opening `build/sphinx/html/index.html`.

[11]: http://sphinx.pocoo.org/
[12]: https://packages.python.org/sphinxcontrib-httpdomain/
[13]: https://docutils.sourceforge.net/rst.html

## Contributing ##

Please report any issues on the [GitHub Issue Tracker][14].

To suggest a change to the code or documentation, please create a new pull
request on GitHub. Contributed code must come with an appropriate unit
test. Please ensure that your code follows [PEP8][15], by running, for example,
[flake8][16] before submitting a pull request. Also, please squash multiple
commits into a single commit in your pull request by [rebasing][17] onto the
master branch.

By contributing to this project, you are agreeing to license your code
contributions under both the GNU Affero General Public License, either version
3 or any later version, and the 3-clause BSD License, and your documentation
contributions under the Creative Commons Attribution-ShareAlike License version
4.0, as described in the copyright license section above.

[14]: http://github.com/mrevutskyi/flask-restless-ng/issues
[15]: https://www.python.org/dev/peps/pep-0008/
[16]: http://flake8.readthedocs.org/en/latest/
[17]: https://help.github.com/articles/about-git-rebase/

## Artwork ##

The `artwork/flask-restless-small.svg` and
`docs/_static/flask-restless-small.png` are licensed under the [Creative
Commons Attribute-ShareAlike 4.0 license][18]. The original image is a scan of
a (now public domain) illustration by Arthur Hopkins in a serial edition of
"The Return of the Native" by Thomas Hardy published in October 1878.

The `artwork/flask-restless.svg` and `docs/_static/flask-restless.png` are
licensed under the [Flask Artwork License][19].

[18]: https://creativecommons.org/licenses/by-sa/4.0
[19]: http://flask.pocoo.org/docs/license/#flask-artwork-license

## Contact ##

Maksym Revutskyi <maksym.revutskyi@gmail.com>
