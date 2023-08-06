#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.command.build_ext import build_ext as _build_ext
from distutils.core import Extension
import os
import sys
import platform
from codecs import open  # To use a consistent encoding

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

APP_NAME = 'thead_tools'

settings = dict()

settings.update(
    name=APP_NAME,
    version=get_version("thead_tools/cmd.py"),
    description='thead linux tools',
    author='Zhuzhg',
    author_email='zzg@ifnfn.com',
    packages=find_packages(),
    install_requires=[
        'pyserial'
    ],

    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    # data_files=[
    #     ('bin', ['thead_tools/build/product64']),
    #     ('bin', ['thead_tools/build/product32']),
    #     ('/usr/local/bin', ['thead_tools/build/product64']),
    #     ('/usr/local/bin', ['thead_tools/build/product32']),
    # ],
    entry_points={
        'console_scripts': [
            'thead = thead_tools.cmd:main',
            # 'cct = thead_tools.cmd:cct_main'
        ],
    },

    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
)


setup(**settings)


architecture = platform.architecture()

if architecture[0] == '64bit':
    product = '/usr/local/bin/product64'
else:
    product = '/usr/local/bin/product32'

try:
    os.symlink(product, '/usr/local/bin/product')
except:
    pass
