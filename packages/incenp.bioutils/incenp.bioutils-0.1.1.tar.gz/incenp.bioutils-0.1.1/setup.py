# -*- coding: utf-8 -*-
# Incenp.Bioutils - Incenp.org's utilities for computational biology
# Copyright © 2020 Damien Goutte-Gattat
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup
from incenp.bio import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='incenp.bioutils',
    version=__version__,
    description='Incenp.org’s utilities for computational biology',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Damien Goutte-Gattat',
    author_email='dgouttegattat@incenp.org',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3'
        ],

    install_requires=[
        'biopython',
        'click',
        'click_shell'
        ],

    extras_require={
        'plasmm': ['reportlab']
        },

    packages=[
        'incenp',
        'incenp.bio',
        'incenp.bio.seq',
        'incenp.bio.modelling'
        ],

    entry_points={
       'console_scripts': [
           'seqtool = incenp.bio.seq.seqtool:seqtool',
           'seqvault = incenp.bio.seq.seqvault:seqvault',
           'cc3d-runner = incenp.bio.modelling.cc3d:main'
           ]
       }
    )
