from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']


setup(
    name='py-harmony',
    version=get_version('py-harmony/__init__.py'),
    url='https://github.com/nolte/py-harmony',
    license='Apache License, Version 2.0',
    author='malte',
    author_email='',
    description='py-harmony',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'requests >= 2.10.0',
        'sleekxmpp >= 1.3.1',
        'argparse >= 1.4.0'
    ],
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
    ],
)
