# -*- coding: utf-8 -*-

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='evileg_core',
    version='0.0.5',
    license='LGPLv3 License',
    description='(ESNF-C) EVILEG Social Network Framework - Core Module.',
    long_description=README,
    url='https://github.com/EVILEG/evileg-core/',
    author='Evgenii Legotckoi',
    author_email='evileg@evileg.com',
    keywords='django evileg core',

    include_package_data=True,
    install_requires=[
        'Django',
        'django-bootstrap4',
        'Markdown',
        'beautifulsoup4',
        'djangocodemirror',
        'requests',
        'redis',
        'django-redis'
    ],
    zip_safe=False,
    packages=['evileg_core'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
