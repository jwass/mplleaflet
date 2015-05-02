try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

DESCRIPTION = "Convert Matplotlib plots into Leaflet web maps"
LONG_DESCRIPTION = DESCRIPTION
NAME = "mplleaflet"
AUTHOR = "Jacob Wasserman"
AUTHOR_EMAIL = "jwasserman@gmail.com"
MAINTAINER = "Jacob Wasserman"
MAINTAINER_EMAIL = "jwasserman@gmail.com"
DOWNLOAD_URL = 'http://github.com/jwass/mplleaflet'
LICENSE = 'BSD 3-clause'
VERSION = '0.0.1'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    url=DOWNLOAD_URL,
    download_url=DOWNLOAD_URL,
    license=LICENSE,
    packages=find_packages(),
    package_data={'': ['*.html']}, # Include the templates
    install_requires=[
        "jinja2",
    ],
)
