# -*- coding: utf-8 -*-
#
#  Copyright 2020 Aleksandr Sizov <murkyrussian@gmail.com>
#  Copyright 2020 Ramil Nugmanov <nougmanoff@protonmail.com>
#  This file is part of MorganFingerprint.
#
#  MorganFingerprint is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
from pathlib import Path
from setuptools import setup, find_packages


version = '1.20'


setup(
    name='MorganFingerprint',
    version=version,
    packages=find_packages(),
    url='https://github.com/dcloudf/MorganFingerprint',
    license='LGPLv3',
    python_requires='>=3.6.0',
    entry_points={'console_scripts': []},
    install_requires=['CGRtools[mrv]>=4.0,<4.1', 'scikit-learn>=0.23', 'numpy>=1.18'],
    extras_require={},
    long_description=(Path(__file__).parent / 'README.md').open().read(),
    classifiers=['Environment :: Plugins',
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'Topic :: Scientific/Engineering :: Chemistry',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 ]
)
