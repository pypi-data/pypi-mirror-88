# -*- coding: utf-8 -*-
# davpoint - Davfs2 wrapper to mount SharePoint filesystems
# Copyright © 2019,2020 Damien Goutte-Gattat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
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
from incenp.davpoint import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='incenp.davpoint',
    version=__version__,
    description='Davfs2 wrapper to mount SharePoint filesystems',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Damien Goutte-Gattat',
    author_email='dgouttegattat@incenp.org',
    url='https://git.incenp.org/damien/davpoint',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
        ],

    install_requires=[
        'click'
        ],

    packages=[
        'incenp',
        'incenp.davpoint'
        ],

    entry_points={
        'console_scripts': [
            'davpoint = incenp.davpoint.__main__:main'
            ]
        }
    )
