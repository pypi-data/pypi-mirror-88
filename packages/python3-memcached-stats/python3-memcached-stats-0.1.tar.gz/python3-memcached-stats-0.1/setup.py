#!/usr/bin/env python
from distutils.core import setup

setup(
    name='python3-memcached-stats',
    version='0.1',
    description='Python3 class to gather stats and slab keys from memcached via the memcached telnet interface',
    author='Daniel Rust, Haoming Huang',
    url='https://github.com/lightningsoon/python3-memcached-stats',
    package_dir={'': 'src'},
    py_modules=[
        'memcached_stats',
    ],
)
