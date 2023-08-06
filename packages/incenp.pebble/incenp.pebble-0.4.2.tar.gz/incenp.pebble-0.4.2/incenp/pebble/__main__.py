# -*- coding: utf-8 -*-
# pebble - Passman client
# Copyright (C) 2018,2019,2020 Damien Goutte-Gattat
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
from click_shell import shell
from incenp.pebble import __version__
from incenp.pebble.cache import Vault
from incenp.pebble.editor import edit_credential
from incenp.pebble.server import Server
from incenp.pebble.util import SecretCache, Error

prog_name = "pbl"
prog_notice = f"""\
{prog_name} (Pebble {__version__})
Copyright © 2018,2019,2020 Damien Goutte-Gattat

This program is released under the GNU General Public License.
See the COPYING file or <http://www.gnu.org/licenses/gpl.html>.
"""


def die(msg):
    print(f"{prog_name}: {msg}", file=sys.stderr)
    sys.exit(1)


def get_server_options(config, section):
    if config.has_option(section, 'server'):
        server_section_name = config.get(section, 'server')
        if not config.has_section(server_section_name):
            die(f"No server section {server_section_name!r} "
                "in configuration file.")
        else:
            return get_server_options(config, server_section_name)
    else:
        host = config.get(section, 'host')
        user = config.get(section, 'user')
        if config.has_option(section, 'password'):
            password = config.get(section, 'password')
        else:
            sc = SecretCache(f"Passphrase for {user} on {host}: ",
                             command=config.get(section, 'password_command',
                                                fallback=None))
            password = sc.get_secret

        return (host, user, password)


def parse_duration(s):
    n = s
    factor = 1
    if len(s) > 1 and s[-1] in ('m', 'h', 'd'):
        n = s[:-1]
        if s[-1] == 'm':
            factor = 60
        elif s[-1] == 'h':
            factor = 3600
        else:
            factor = 86400

    try:
        return int(n) * factor
    except ValueError:
        die(f"Improper duration value: {s}")


@shell(prompt="pbl> ",
       context_settings={'help_option_names': ['-h', '--help']})
@click.option('--config', '-c', type=click.Path(exists=True),
              default='{}/config'.format(click.get_app_dir('pebble')),
              help="Path to an alternative configuration file.")
@click.option('--section', '-s', default='default',
              help="Name of the configuration file section to use.")
@click.option('--refresh', '-f', is_flag=True, default=False,
              help="Always refresh the local cache.")
@click.option('--no-refresh', is_flag=True, default=False,
              help="Never refresh the cache even if it is old.")
@click.version_option(version=__version__, message=prog_notice)
@click.pass_context
def pebble(ctx, config, section, refresh, no_refresh):
    """Command-line client for Nextcloud’s Passman."""

    cfg = ConfigParser()
    cfg.read(config)

    home_dir = os.getenv('HOME', default='')
    data_dir = '{}/pebble'.format(
        os.getenv('XDG_DATA_HOME',
                  default='{}/.local/share'.format(home_dir)))

    if not cfg.has_section(section):
        die(f"No section {section!r} in configuration file.")

    vault_name = cfg.get(section, 'vault')
    server = Server(*get_server_options(cfg, section))
    sc = SecretCache(f"Passphrase for vault {vault_name} on "
                     f"{server.user}@{server.host}: ")
    caching = not(cfg.getboolean(section, 'nocache', fallback=False))
    vault = Vault(server, vault_name, data_dir, sc.get_secret,
                  caching=caching)

    if refresh:
        max_age = 0
    elif no_refresh:
        max_age = -1
    else:
        max_age_s = cfg.get(section, 'max_age', fallback='86400')
        max_age = parse_duration(max_age_s)

    vault.load(max_age)

    ctx.obj = vault
    ctx.call_on_close(server.close)


@pebble.command()
@click.argument('crid', type=click.INT)
@click.pass_obj
def delete(vault, crid):
    """Delete a credential.
    
    This command deletes the credential with the specified credential
    ID.
    """

    cred = vault.get(crid)
    if not cred:
        raise Error(f"No credential found with ID {crid}")
    answer = input(f"Really delete credential {cred['label']!r} (y/N)? ")
    if answer == 'y':
        vault.delete(cred)


@pebble.command()
@click.argument('crid', type=click.INT)
@click.option('--json', '-j', is_flag=True, default=False,
              help="Edit credential as JSON.")
@click.pass_obj
def edit(vault, crid, json):
    """Edit an existing credential.
    
    This command allows to modify the credential with the specified
    credential ID.
    """

    cred = vault.get(crid, decrypt=True)
    if not cred:
        raise Error(f"No credential found with ID {crid}.")
    updated = edit_credential(cred, as_json=json)
    if updated:
        vault.update(updated)
    else:
        print("No changes.")


@pebble.command('list')
@click.argument('patterns', nargs=-1)
@click.option('--id', '-i', 'with_id', is_flag=True, default=False,
              help="Display credential IDs.")
@click.pass_obj
def list_credentials(vault, patterns, with_id):
    """List credentials.
    
    This command lists the credentials matching the given pattern(s);
    if no pattern are given, all credentials are listed.
    """

    creds = vault.search(patterns)
    for cred in creds:
        if with_id:
            print(f"{cred['credential_id']}: {cred['label']}")
        else:
            print(cred['label'])


@pebble.command()
@click.option('--json', '-j', is_flag=True, default=False,
              help="Edit new credential as JSON.")
@click.pass_obj
def new(vault, json):
    """Create a new credential.
    
    This command adds a new credential to the store.
    """

    template = {
        'label': '',
        'description': '',
        'created': None,
        'changed': None,
        'tags': [],
        'email': '',
        'username': '',
        'password': '',
        'url': '',
        'favicon': '',
        'renew_interval': 0,
        'expire_time': 0,
        'delete_time': 0,
        'files': [],
        'custom_fields': [],
        'otp': {},
        'hidden': False
        }
    newcred = edit_credential(template, json)
    if newcred:
        if vault.test_decryption():
            vault.add(newcred)
    else:
        print("No changes.")


@pebble.command()
@click.pass_obj
def refresh(vault):
    """Refresh the cache.
    
    This command refreshes the local cache from the server.
    """

    vault.load(0)


_fields = [
    ('description', 'Description', None),
    ('tags', 'Tags', lambda tags: ', '.join([tag[u'text'] for tag in tags])),
    ('url', 'URL', None),
    ('username', 'URL', None),
    ('email', 'Email', None),
    ('password', 'Password', None)
    ]


@pebble.command()
@click.argument('patterns', nargs=-1)
@click.option('--id', '-i', 'show_id', default=-1, type=click.INT,
              metavar="ID",
              help="Show the credential with the specified ID.")
@click.pass_obj
def show(vault, patterns, show_id):
    """Show credential(s).
    
    This command shows the credentials matching the given pattern(s);
    if no pattern is given, all credentials are shown.
    """

    if show_id != -1:
        creds = [vault.get(show_id, decrypt=True)]
    else:
        creds = vault.search(patterns, decrypt=True)
    for cred in creds:
        print(f"+---- {cred['label']} ({cred['credential_id']}) -----")
        for field_name, field_label, field_format in _fields:
            if cred[field_name]:
                if field_format:
                    formatted_field = field_format(cred[field_name])
                else:
                    formatted_field = cred[field_name]
                print(f"| {field_label}: {formatted_field}")
        if cred['custom_fields']:
            for custom in cred['custom_fields']:
                print(f"| {custom['label']}: {custom['value']}")
        print("+----")


if __name__ == '__main__':
    pebble()
