#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


with open('README.rst') as readme_file:
    readme = readme_file.read()


with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as req_file:
    requirements = req_file.read().splitlines()

with open('requirements_dev.txt') as dev_req_file:
    setup_requirements = dev_req_file.read().splitlines()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

test_requirements = []

setup(
    author="Lars Claussen",
    author_email='claussen.lars@nelen-schuurmans.nl',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="websocket client for threedi websocket consumer endpoints",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'active_simulations=threedi_ws_client.commands.active_simulations:run',
        ],
    },
    keywords='threedi_ws_client',
    name='threedi-ws-client',
    packages=find_packages(include=['threedi_ws_client', 'threedi_ws_client.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/larsclaussen/threedi-ws-client',
    version=find_version('threedi_ws_client', 'version.py'),
    zip_safe=False,
)
