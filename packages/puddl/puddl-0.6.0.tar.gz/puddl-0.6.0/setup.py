#!/usr/bin/env python
from setuptools import setup, find_packages, find_namespace_packages

setup(
    packages=find_packages() + find_namespace_packages(include=['puddl.*']),
    install_requires=[
        'Click',
        'flask',
        'ffmpeg-python',
        'filetype',
        'pandas',
        'psycopg2-binary',
        'requests',
        'sqlalchemy',
        'tinytag',
    ],
    entry_points='''
        [console_scripts]
        puddl=puddl.cli:main
    ''',
)
