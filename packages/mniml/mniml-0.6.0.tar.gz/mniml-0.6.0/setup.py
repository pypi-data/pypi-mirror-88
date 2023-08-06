# -*- coding: utf-8 -*-

'''A setuptools-based setup module.

See https://packaging.python.org/distributing/

See:
https://pypi.python.org/pypi?%3Aaction=list_classifiers
... for list of trove classifiers

'''


from codecs import open
from os import path
from setuptools import setup, find_packages


# See https://github.com/pypa/sampleproject/setup.py
root = path.abspath(path.dirname(__file__))

with open(path.join(root, 'README.rst'), encoding='utf-8') as f:
    long_description = 'Not for use'

with open(path.join(root, 'LICENSE.txt'), encoding='utf-8') as f:
    license = f.read()

with open(path.join(root, 'VERSION.txt'), encoding='utf-8') as f:
    version = f.read().strip()



setup(
    name='mniml',
    # See https://packaging.python.org/single_source_version/
    python_requires='>=3.7',
    version=version,
    long_description_content_type='text/markdown',
    description='A minimal Python package',
    long_description=long_description,
    url='https://github.com/geoffrey-a-reed/minimal',
    author='Geoffrey A. Reed',
    author_email='evansj@email.chop.edu',
    license=license,
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='sample setuptools development',
    packages=['mniml'],
    install_requires=['apache-beam[gcp]'],
    package_data={
        '': ['VERSION.txt', 'LICENSE.txt']
    },
)
