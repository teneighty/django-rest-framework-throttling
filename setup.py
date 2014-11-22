#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

import os
import re
import sys

# This command has been borrowed from and rest_framework
# https://github.com/getsentry/sentry/blob/master/setup.py
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def get_version(package):
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

version = get_version('rest_framework_throttling')

setup(
    name='djangorestframeworkthottling',
    version=version,
    url='http://www.django-rest-framework.org',
    license='BSD',
    description='Web APIs for Django, made easy.',
    author='Tim Horton',
    author_email='tim@airbitz.co',
    cmdclass={'test': PyTest},
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 1 - Development/Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
