# -*- coding: utf-8 -*-
import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

# Determine version of this application.
PKG = "keep"
VERSIONFILE = os.path.join(PKG, "version.py") 
version = "unknown"
try: 
    version_file = open(VERSIONFILE, "r")
    for line in version_file:
        if '__version__' in line:
            version = line.split("'")[1]
            break
except EnvironmentError:
    pass # Okay, there is no version file.

setup(
    name = 'keep',
    version = version,
    description = '',
    author = 'Project Keep',
    author_email = '',
    include_package_data=True,
    install_requires = [
        "falcon",
        "mock",
        "wsgiref",
        "uWSGI",
        "pymongo",
    ],
    test_suite = 'keep.tests',
    zip_safe = False,
    scripts=['bin/startkeep'],
    packages = find_packages(exclude=['ez_setup'])
)
