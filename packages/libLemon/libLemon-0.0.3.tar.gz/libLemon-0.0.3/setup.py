#!/usr/bin/env python
# encoding: utf-8
"""
@license: GPL-v3
@software: lemon-lite
"""

from setuptools import setup, find_packages
from libLemon.Utils.Const import VERSION


def parse_dependencies(req_path: str = './libLemon/requirements.txt') -> list[str]:
    return [l.strip() for l in open(req_path).readlines() if l.strip()]


setup(
    name='libLemon',
    version=VERSION,
    description=(
        'Lightweight shipborne modular control library.'
    ),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.9',
    author='sjtu-lime',
    author_email='akaza_akari@sjtu.edu.cn',
    maintainer='sjtu-lime',
    maintainer_email='akaza_akari@sjtu.edu.cn',
    license='GNU General Public License v3.0',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/sjtu-lime',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=parse_dependencies()
)
