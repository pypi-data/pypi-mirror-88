"""About datarobot
=========================
.. image:: https://img.shields.io/pypi/v/datarobot.svg
   :target: https://pypi.python.org/pypi/datarobot/
.. image:: https://img.shields.io/pypi/pyversions/datarobot.svg
.. image:: https://img.shields.io/pypi/status/datarobot.svg

DataRobot is a client library for working with the `DataRobot`_ platform API.

Installation
=========================
Python 2.7 and >= 3.4 are supported.
You must have a datarobot account.

::

   $ pip install datarobot

Usage
=========================
The library will look for a config file `~/.config/datarobot/drconfig.yaml` by default.
This is an example of what that config file should look like.

::

   token: your_token
   endpoint: https://app.datarobot.com/api/v2

Alternatively a global client can be set in the code.

::

   import datarobot as dr
   dr.Client(token='your_token', endpoint='https://app.datarobot.com/api/v2')

Alternatively environment variables can be used.

::

   export DATAROBOT_API_TOKEN='your_token'
   export DATAROBOT_ENDPOINT='https://app.datarobot.com/api/v2'

See `documentation`_ for example usage after configuring.

Tests
=========================
::

   $ py.test

.. _datarobot: http://datarobot.com
.. _documentation: https://datarobot-public-api-client.readthedocs-hosted.com
"""

import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


with open("datarobot/_version.py") as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("Cannot find version information")


tests_require = [
    "mock==3.0.5",
    "pytest>=4.6,<5",  # 4.6 is last release supporting python2
    "pytest-cov",
    "responses>=0.9,<0.10",  # 0.10 changes the interface, will require test changes
]

dev_require = tests_require + [
    "flake8>=2.5.2,<3",
    "Sphinx==1.8.3",
    "sphinx_rtd_theme==0.1.9",
    "nbsphinx>=0.2.9,<1",
    "nbconvert==5.3.1",
    "numpydoc>=0.6.0",
    "tox",
    "jupyter_contrib_nbextensions",
    "tornado<6.0",
    'black==19.10b0; python_version >= "3.6"',
    'isort==5.4.2; python_version >= "3.6"',
]

example_require = [
    "jupyter<=5.0",
    "fredapi==0.4.0",
    "matplotlib>=2.1.0",
    "seaborn<=0.8",
    "sklearn<=0.18.2",
    "wordcloud<=1.3.1",
    "colour<=0.1.4",
]

release_require = ["zest.releaser[recommended]==6.22.0"]

setup(
    name="datarobot",
    version=version,
    description="This client library is designed to support the DataRobot API.",
    author="datarobot",
    author_email="support@datarobot.com",
    maintainer="datarobot",
    maintainer_email="info@datarobot.com",
    url="http://datarobot.com",
    license="Apache Software License",
    packages=[
        "datarobot",
        "datarobot._experimental",
        "datarobot._experimental.models",
        "datarobot.models",
        "datarobot.models.external_dataset_scores_insights",
        "datarobot.models.visualai",
        "datarobot.utils",
        "datarobot.helpers",
        "datarobot.ext",
    ],
    long_description=__doc__,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        "contextlib2>=0.5.5",
        "pandas>=0.15",
        "pyyaml>=3.11",
        "requests>=2.21",
        "requests_toolbelt>=0.6",
        "trafaret>=0.7,<2.0,!=1.1.0",
        "urllib3>=1.23",
        "attrs>=19.1.0,<20.0",
    ],
    tests_require=tests_require,
    extras_require={"dev": dev_require, "examples": example_require, "release": release_require},
    cmdclass={"test": PyTest},
)
