import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from _mplleaflet_setup import (require_clean_submodules, UpdateSubmodules)

with open('AUTHORS.md') as f:
    authors = f.read()

description = "Convert Matplotlib plots into Leaflet web maps"
long_description = description + "\n\n" + authors
NAME = "mplleaflet"
AUTHOR = "Jacob Wasserman"
AUTHOR_EMAIL = "jwasserman@gmail.com"
MAINTAINER = "Jacob Wasserman"
MAINTAINER_EMAIL = "jwasserman@gmail.com"
DOWNLOAD_URL = 'http://github.com/jwass/mplleaflet'
LICENSE = 'BSD 3-clause'
VERSION = '0.0.5'

# Make sure submodules are updated and synced
root_dir = os.path.abspath(os.path.dirname(__file__))
require_clean_submodules(root_dir, sys.argv)

setup(
    name=NAME,
    version=VERSION,
    description=description,
    long_description=long_description,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    url=DOWNLOAD_URL,
    download_url=DOWNLOAD_URL,
    license=LICENSE,
    cmdclass={'submodule': UpdateSubmodules},
    packages=list(set(find_packages() + ["mplleaflet","mplleaflet/mplexporter","mplleaflet/mplexporter/renderers"])),
    package_data={'': ['*.html']}, # Include the templates
    install_requires=[
        "jinja2",
        "six",
        "ipython",
    ],
)
