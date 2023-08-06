#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from functools import wraps

from setuptools import find_packages
from setuptools import setup

from ast import literal_eval
import os
DOCKER_DEV = literal_eval(os.environ.get("DEV_TENSORFREE", "0"))


def safe_dev_read(func):
    @wraps(func)
    def wrapper(*a, **k):
        try:
            return func(*a, **k)
        except FileNotFoundError:
            if DOCKER_DEV:
                return ""
            raise
    return wrapper


@safe_dev_read
def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='tensorfree',
    use_scm_version={
        'local_scheme': 'dirty-tag',
        'write_to': 'src/tensorfree/_version.py',
        'fallback_version': '0.0.0',
    } if not DOCKER_DEV else False,
    license='MIT',
    description='Tensorfree is an image classification library that provides quick and easy access to some of the latest SOTA models. Simply install, define the location of your photos and let it do everything for you.',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Andrew Smith',
    author_email='asmith@g.harvard.edu',
    url='https://github.com/andrew-alm/tensorfree',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        # Issue with setuptools_scm with these versions, exploring solutions
        # 'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
    project_urls={
        'Issue Tracker': 'https://github.com/andrew-alm/tensorfree/issues',
    },
    keywords=[
        'image classification', 'tensorflow', 'keras'
    ],
    python_requires='>=3.6',
    install_requires=[
        'tensorflow',
        'keras',
        'numpy',
        'pillow',
        'setuptools_scm'
    ],
    extras_require={
    },
    setup_requires=[
        'setuptools_scm>=3.3.1',
    ],
    entry_points={
        'console_scripts': [
            'tensorfree = tensorfree.cli:main',
        ]
    },
)
