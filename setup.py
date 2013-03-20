# -*- coding: utf-8 -*-
import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

# Determine version of this application.
# TBD: Revisit version flows and processing once integrating with OpenStack, see glance setup.py
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

class local_sdist(sdist):
    """Customized sdist hook - builds the ChangeLog file from VC first"""

        def run(self):
            sdist.run(self)

cmdclass = {'sdist': local_sdist}

# TDB: Revisit sphinx documentation needs once move to OpenStack...see glance setup.py

setup(
    name = 'keep',
    version = version,
    description = 'The Keep project provides a service for storing '
                  'sensitive client information such as encryption keys',
    license='Apache License (2.0)',
    author = 'OpenStack',
    author_email = 'john.wood@rackspace.com',
    url='http://keep.openstack.org/',
    packages = find_packages(exclude=['bin']),
    test_suite = 'nose.collector',
    cmdclass=cmdclass,
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Environment :: No Input/Output (Daemon)',
    ],
    scripts=['bin/keep-api'],
    py_modules=[]
)
