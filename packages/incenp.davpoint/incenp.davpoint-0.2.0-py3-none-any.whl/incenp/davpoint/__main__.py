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

from configparser import ConfigParser
import os
import sys

import click

from incenp.davpoint import __version__
from incenp.davpoint.davfs2 import get_credentials, mount
from incenp.davpoint.sharepoint import authenticate

prog_name = "davpoint"
prog_notice = f"""\
{prog_name} {__version__}
Copyright © 2019,2020 Damien Goutte-Gattat

This program is released under the GNU General Public License.
See the COPYING file or <http://www.gnu.org/licenses/gpl.html>.
"""


def die(msg):
    print(f"{prog_name}: {msg}", file=sys.stderr)
    sys.exit(1)


@click.command('davpoint',
               epilog="Report bugs to <devel@incenp.org>.")
@click.option('--config', '-c', 'config_file',
              type=click.Path(exists=True),
              default='{}/.davfs2/sharepoint.conf'.format(
                  os.getenv('HOME', default='.')),
              help="Path to an alternative configuration file.")
@click.version_option(version=__version__, message=prog_notice)
@click.argument('share')
def main(config_file, share):
    """Mount SharePoint remote filesystems."""

    config = ConfigParser()
    config.read(config_file)

    if not config.has_section(share):
        die(f"No section {share!r} in configuration file")

    endpoint = config.get(share, 'endpoint')
    mountpoint = config.get(share, 'mountpoint')

    davfs2_options = {}
    for key, value in config.items(share):
        if key not in ('endpoint', 'mountpoint'):
            davfs2_options[key] = value

    username, password = get_credentials(endpoint, mountpoint)
    cookies = authenticate(endpoint, username, password)
    davfs2_options['add_header'] = (f'Cookie rtFa={cookies["rtFa"]};'
                                    f'FedAuth={cookies["FedAuth"]};')

    mount(mountpoint, davfs2_options)


if __name__ == '__main__':
    main()
