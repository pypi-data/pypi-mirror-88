#!/usr/bin/env python

# © Copyright IBM Corporation 2020.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools.command.test import test as TestCommand
import os
import sys
import pkg_resources
import setuptools

__version__ = '0.1.0'
PACKAGE_NAME = 'ibp-python-sdk'
PACKAGE_DESC = 'Python client library for IBM Blockchain Platform'

if sys.argv[-1] == 'publish':
    # test server
    os.system('python setup.py register -r pypitest')
    os.system('python setup.py sdist upload -r pypitest')

    # production server
    os.system('python setup.py register -r pypi')
    os.system('python setup.py sdist upload -r pypi')
    sys.exit()

with open('README.md', 'r', encoding='utf-8') as fh:
    readme = fh.read()

setuptools.setup(
    name=PACKAGE_NAME.replace('_', '-'),
    version=__version__,
    author='IBM',
    author_email='no-reply@ibm.com',
    description=PACKAGE_DESC,
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/IBM-Blockchain/ibp-python-sdk',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    python_requires='>=3.5',
    license='Apache 2.0',
    keywords=PACKAGE_NAME,
)
