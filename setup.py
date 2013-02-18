#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='economics',
      version='0.0.1',
      description='Implementation of basic classical economics',
      author='Juan Reyero',
      author_email='juan@juanreyero.com',
      url='http://juanreyero.com/',
      packages=['economics'],
      test_suite='economics.test.econ_test.suite')
