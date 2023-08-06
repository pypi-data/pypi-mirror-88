#!/usr/bin/env python3

"""Python packaging for repo."""

from __future__ import print_function

import os
import setuptools


TOPDIR = os.path.dirname(os.path.abspath(__file__))


# Rip out the first intro paragraph.
with open(os.path.join(TOPDIR, 'README.md')) as fp:
    lines = fp.read().splitlines()[2:]
    end = lines.index('')
    long_description = ' '.join(lines[0:end])


# https://packaging.python.org/tutorials/packaging-projects/
setuptools.setup(
    name='esrlabs-auto-update',
    version='0.1.0',
    maintainer='Maksim',
    maintainer_email='maksim.danilov@esrlabs.com',
    description='ESR Labs AutoUpdate automatically updates tools to latest version',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mdanilov/esrlabs-auto-update',
    project_urls={
        'Bug Tracker': 'https://github.com/mdanilov/esrlabs-auto-update/issues',
    },
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    install_requires=['python-crontab'],
)
