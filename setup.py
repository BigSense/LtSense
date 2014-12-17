#!/usr/bin/env python
"""
Copyright [2014] [http://bigsense.io]

This file is part of LtSense.

LtSense is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LtSense is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LtSense.  If not, see <http://www.gnu.org/licenses/>.
"""

from distutils.core import setup
import os

setup(
    name='ltsense',
    version=os.popen('git describe --dirty').readlines()[0].strip(),
    packages=['ltsense'],
    author='Sumit Khanna',
    author_email='sumit@penguindreams.org',
    url='http://bigsense.io',
    license='GNU General Public License v3',
    long_description=open('README').read(),
    scripts=['scripts/ltsense'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Topic :: Scientific/Engineering :: GIS',
    ]
)