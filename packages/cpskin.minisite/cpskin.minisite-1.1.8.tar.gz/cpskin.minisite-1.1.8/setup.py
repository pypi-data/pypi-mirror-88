# -*- coding: utf-8 -*-

version = '1.1.8'

from setuptools import setup, find_packages

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(
    name='cpskin.minisite',
    version=version,
    description="UI for sections configured with their own domain",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Framework :: Zope2",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='IMIO',
    author_email='support@imio.be',
    url='https://github.com/imio/',
    license='gpl',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Plone',
        'plone.api',
        'collective.weightedportlets',
        'plone.app.contenttypes',
        'cpskin.core',
        'cpskin.locales',
        'plone.rest',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.robotframework [debug]',
            'cpskin.workflow',
            'cpskin.core [test]',
        ],
    },
    entry_points={},
)
