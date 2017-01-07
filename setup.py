from setuptools import setup, find_packages

import unittest

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

with open("requirements-tests.txt", 'r') as f:
    test_requirements = f.read().split('\n')
with open("requirements.txt", 'r') as f:
    requirements = f.read().split('\n')

setup(
    name='py_proj_lights',
    version='1.0',
    packages= find_packages(),
    url='https://github.com/DrimTim32/py_proj_transport',
    license='MIT',
    author='gese anna, sobol bartek, malinowski marcin',
    author_email='',
    description='',
    test_suite='setup.my_test_suite',
    setup_requires=requirements,
    tests_require=test_requirements
)
