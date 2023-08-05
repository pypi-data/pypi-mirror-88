#!/usr/bin/env python

#  Copyright (c) 2020, László Hegedűs <laszlo.hegedus@cherubits.hu>
#   All Rights Reserved.
#   NOTICE:  All information contained herein is, and remains the property of László Hegedűs  and its
#   suppliers,  if any.  The intellectual and technical concepts contained herein are proprietary to
#   László Hegedűs  and its suppliers and may be covered by Hungarian Republic  and Foreign Patents,  patents
#   in process, and are protected by trade secret or copyright law. Dissemination of this information or
#   reproduction of this material  is strictly forbidden unless prior written permission is obtained
#   from László Hegedűs.

import os
import sys

from setuptools import find_packages, setup


import os
from distutils.util import convert_path
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def parse_requirements(filename):
    with open(filename) as f:
        return [line for line in f.read().splitlines() if not line.startswith('#')]


# ========================================
# Parse requirements for all configuration
# ========================================
install_reqs = parse_requirements(filename=os.path.join('.', 'requirements.txt'))
reqs = [str(ir) for ir in install_reqs]

# ========================================
# Readme
# ========================================
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

PROJECT_NAME = 'nuclear-postaladdress'

# ========================================
# Version parsing
# ========================================
main_ns = {}
ver_path = convert_path('postaladdress/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='nuclear-postaladdress',
    version=main_ns['__version__'],
    author='László Hegedűs',
    author_email='laszlo.hegedus@cherubits.hu',
    maintainer='László Hegedűs',
    maintainer_email='laszlo.hegedus@cherubits.hu',
    url='https://gitlab.com/cherubits/cherubits-community/nuclear-platform/nuclear-postaladdress',
    description='A django application for describing addresses.',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Database',
        'Topic :: Utilities'
    ],
    license='MIT',
    packages=find_packages(exclude=[
        'person',
        'person.*',
        'person.migrations.*',
        'person.templates.*',
        'example_site'
        'example_site.*'
    ]),
    include_package_data=True,
    package_data={'': ['*.js']},
    install_requires=reqs,
    zip_safe=False,

)
