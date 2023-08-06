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

"""Davfs2 helper module.

This module provides functions to call the mount.davfs tool and to
read its configuration.
"""

from os import fdopen, geteuid, getenv, rename, unlink
from os.path import exists
from tempfile import mkstemp
from subprocess import call

from incenp.davpoint import Error


def _get_secrets_filename():
    if geteuid() == 0:
        return '/etc/davfs2/secrets'
    else:
        return '{}/.davfs2/secrets'.format(getenv('HOME', default='.'))


def _parse_secrets_line(line):
    fields = []
    in_quote = False
    escaped = False
    field = ''
    for c in line:
        if in_quote:
            if c == '"' and not escaped:
                in_quote = False
                fields.append(field)
                field = ''
            else:
                field += c
        elif escaped:
            if c in (' ', '\t', '#', '\\', '"'):
                field += c
                escaped = False
            else:
                field += '\\'
                field += c
                escaped = False
        elif c in (' ', '\t', '\n'):
            fields.append(field)
            field = ''
        else:
            field += c
    return fields


def _parse_secrets_file(filename):
    secrets = []
    with open(filename, 'r') as f:
        for line in f:
            if len(line) == 0:
                continue
            if line.startswith('#'):
                continue
            secrets.append(_parse_secrets_line(line))
    return secrets


def get_credentials(endpoint, mountpoint):
    """Get the username and password associated to a WebDAV resource.

    This function reads Davfs2's secrets file to obtain the credentials
    associated with either a WebDAV endpoint or a mountpoint.
    """
    secrets_file = _get_secrets_filename()
    secrets = _parse_secrets_file(secrets_file)
    for secret in secrets:
        if len(secret) != 3:
            continue
        if secret[0] in (endpoint, mountpoint):
            return (secret[1], secret[2])
    raise Error(f"Credentials not found for {endpoint}:{mountpoint}")


def mount(mountpoint, config):
    """Mount a WebDAV resource.

    This function calls the mount (8) command to mount the WebDAV
    resource associated with the specified endpoint. Options to the
    mount.davfs program may be given in the config dictionary.
    """
    backup = None
    command = ['mount', mountpoint]

    if geteuid() == 0:
        # Write configuration to a temporary file
        fd, fn = mkstemp(text=True)
        fh = fdopen(fd, 'w')
        command.insert(1, '-o')
        command.insert(2, f'conf={fn}')
    else:
        # Write configuration to ~/.davfs2/davfs2.conf
        # (Backup it first if it exists)
        fn = '{}/.davfs2/davfs2.conf'.format(getenv('HOME', '.'))
        if exists(fn):
            backup = f'{fn}.bak'
            rename(fn, backup)
        fh = open(fn, 'w')

    for key, value in config.items():
        fh.write(f'{key} {value}\n')
    fh.close()

    ret = call(command)
    unlink(fn)

    if backup:
        rename(backup, fn)

    return ret
