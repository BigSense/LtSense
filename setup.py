#!/usr/bin/env python
"""
Copyright [2015] [http://bigsense.io]

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

from setuptools import setup, find_packages
import os
import platform
import math


def init_system():
    """
    Returns a tuple of init data files and a version suffix (deb only).
    Example: (('/etc/init/', ['scripts/upstart/ltsense.conf']),'~upstart')
    """
    distro = os.getenv('DISTRO', platform.linux_distribution()[0])
    release = os.getenv('RELEASE', platform.linux_distribution()[1])
    if distro == 'Ubuntu':
        return (('/etc/init/', ['scripts/upstart/ltsense.conf']),
                '~upstart')
    elif distro in ['debian']:
        release_int = int(math.floor(float(release)))
        if release_int == 7:
            return (('/etc/init.d/', ['scripts/systemv/ltsense']),
                   '~systemv')
        elif release_int == 8:
            return (('/lib/systemd/system/', ['scripts/systemd/ltsense.service']),
                   '~systemd')
    elif distro in ['centos', 'redhat', 'fedora']:
        return (('/lib/systemd/system/', ['scripts/systemd/ltsense.service']),'')

setup(
    name='ltsense',
    version='{}{}'.format(os.popen('git describe --dirty').readlines()[0].strip(),init_system()[1]),
    packages=find_packages(),
    author='Sumit Khanna',
    author_email='sumit@penguindreams.org',
    maintainer='Sumit Khanna',
    maintainer_email='sumit@penguindreams.org',
    url='http://bigsense.io',
    license='GNU General Public License v3',
    description='ltsense sensor collection and relay service',
    long_description=open('README').read(),
    data_files=[init_system()[0],
                ('/etc/ltsense/examples', ['etc/virtual-ltsense.conf',
                                           'etc/onewire-ltsense.conf'])
                ],
    entry_points={'console_scripts': ['ltsense=ltsense.__main__:main']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    install_requires=['configobj>=4.7.2']
)
