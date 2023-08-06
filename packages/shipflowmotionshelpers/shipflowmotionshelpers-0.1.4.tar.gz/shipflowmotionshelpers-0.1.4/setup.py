#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import versioneer

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = ['pytest-runner', 'versioneer']

test_requirements = ['pytest>=3', ]

setup(
    author="Martin Alexandersson",
    author_email='maralex@chalmers.se',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python helper function for ShipFlow Motions",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='shipflowmotionshelpers',
    name='shipflowmotionshelpers',
    packages=find_packages(include=['shipflowmotionshelpers', 'shipflowmotionshelpers.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/martinlarsalbert/shipflowmotionshelpers',
    zip_safe=False,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
