Calibration Client
==================

Calcat is the Web App design for Calibration Constants Data Management
at European XFEL.

This library (calibration_client) is a client for the RESTful APIs exposed
by the European XFEL Calibration Constants Catalogue Web Application - calCat
(https://in.xfel.eu/calibration).

*Repository:*

 * https://git.xfel.eu/gitlab/ITDM/calibration_client

*Dependencies:*

- oauthlib (https://pypi.python.org/pypi/oauthlib)
- requests (https://github.com/kennethreitz/requests)
- requests-oauthlib (https://github.com/requests/requests-oauthlib)
- oauth2_xfel_client (https://git.xfel.eu/gitlab/ITDM/oauth2_xfel_client)
- pytz (https://pypi.org/project/pytz/)

Installation
------------

Python project
""""""""""""""

1. Install requirements, if never done before

 1.1. For OS X distributions::

  1.1.1. Homebrew

        brew install python3

  1.1.2 Port

        sudo port install python36

        sudo port select --set python3 python36

        sudo port install py36-pip
        sudo port select --set pip pip36

 1.2. For Linux distributions::

    sudo apt-get update
    sudo apt-get install python3.6

2. Make calibration_client library available in your python environment

 2.1. Install it via pip::

    # Install dependencies from local wheels files
    pip install . --no-index --find-links ./external_dependencies/

    # Install dependencies from the pypi
    pip install .

 Installing it will place two folders under the current Python installation
 site-packages folder:

 - `calibration_client` with the sources;
 - `calibration_client-9.0.2.dist-info/` with Wheels configuration files.

 To identify your Python site-packages folder run::

    python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"


Usage
-----

To use this project you need to import it::

    from calibration_client import CalibrationClient


Development & Testing
---------------------

When developing, and before commit changes, please validate that:

1. All tests continue passing successfully (to validate that run *pytest*)::

    # Go to the source code directory
    cd calibration_client

    # Upgrade package and all its required packages
    pip install . -U --upgrade-strategy eager

    # Install test dependencies
    pip install '.[test]' -U --upgrade-strategy eager

    # Run all tests using pytest
    pytest

    # Run all tests and get information about coverage for all files inside calibration_client package
    pytest --cov calibration_client --cov-report term-missing

2. Code keeps respecting pycodestyle code conventions (to validate that run **pycodestyle**)::

    pycodestyle .

3. To generate all the wheels files for the dependencies, execute::

    # Generate Wheels to itself and dependencies
    pip wheel --wheel-dir=./external_dependencies .
    pip wheel --wheel-dir=./external_dependencies --find-links=./external_dependencies .

4. Check that you have the desired dependency versions in ``external_dependencies`` folder, since no versions are now set in ``setup.py``.


Registering library on https://pypi.org
---------------------------------------

To register this python library, the following steps are necessary::

    # Install twine
    python -m pip install --upgrade twine

    # Generates source distribution (.tar.gz) and wheel (.whl) files in the dist/ folder
    python setup.py sdist
    python setup.py bdist_wheel

    # Upload new version .egg and .whl files
    twine upload dist/*

    # In case a test is necessary, it is possible to test it against test.pypi.org
    twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose
