#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='simple_menus',
    version='1.10',
    packages=find_packages(),
    include_package_data=True,
    license='zlib/libpng License',
    description='A Django app for menus with nested links.',
    url='https://github.com/russelljk/simple_menus',
    author='Russell Kyle',
    author_email='russell.j.kyle@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: zlib/libpng License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
