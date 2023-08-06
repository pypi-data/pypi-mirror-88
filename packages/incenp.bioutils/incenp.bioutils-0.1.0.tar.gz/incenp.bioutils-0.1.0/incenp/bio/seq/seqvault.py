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

"""A tool to access a BioSQL-based sequence database."""

from configparser import ConfigParser
from hashlib import md5
import os.path
from subprocess import run
import sys
from tempfile import NamedTemporaryFile

from Bio import SeqIO
from BioSQL.BioSeqDatabase import open_database
import click
from click_shell import shell
from incenp.bio import __version__
from incenp.bio.seq import vault
from incenp.bio.seq.usa import parse_usa, write_usa

prog_name = "seqvault"
prog_notice = f"""\
{prog_name} {__version__}
Copyright © 2020 Damien Goutte-Gattat

This program is released under the GNU General Public License.
See the COPYING file or <http://www.gnu.org/licenses/gpl.html>.
"""

default_config = '{}/seqvault.rc'.format(click.get_app_dir('seqvault'))


def _get_database(ctx, param, value):
    try:
        return ctx.obj[value]
    except KeyError:
        raise click.BadParameter(f"No {value!r} database on the server")


def _get_usa(ctx, param, value):
    try:
        return parse_usa(value)
    except Exception as e:
        raise click.BadParameter(f"Invalid USA: {e}")


def _get_usas(ctx, param, value):
    try:
        return [parse_usa(usa) for usa in value]
    except Exception as e:
        raise click.BadParameter(f"Invalid USA: {e}")


def _check_config_file(ctx, param, value):
    if value != default_config and not os.path.exists(value):
        raise click.BadParameter(f"Specified config file {value!r} not found")
    return value


@shell(context_settings={'help_option_names': ['-h', '--help']},
       prompt=f"{prog_name}> ")
@click.option('--config', '-c', type=click.Path(), default=default_config,
              callback=_check_config_file,
              help="Path to the configuration file.")
@click.option('--driver', metavar="DRIVER",
              help="Specify the database driver.")
@click.option('--host', '-H', metavar="HOST",
              help="Specify the database host.")
@click.option('--user', '-u', metavar="USER",
              help="Specify the database user name.")
@click.option('--name', '-n', metavar="NAME",
              help="Specify the database name.")
@click.version_option(version=__version__, message=prog_notice)
@click.pass_context
def seqvault(ctx, config, driver, host, user, name):
    """Access a BioSQL sequence database."""

    cfg = ConfigParser()
    cfg.add_section('Server')
    cfg.set('Server', 'driver', 'psycopg2')
    cfg.set('Server', 'host', 'localhost')
    cfg.set('Server', 'user', 'seqvault')
    cfg.set('Server', 'database', 'seqvault')

    try:
        cfg.read(config)
    except Exception as e:
        raise click.ClickException(f"Cannot read configuration file: {e}")

    if driver:
        cfg.set('Server', 'driver', driver)
    if host:
        cfg.set('Server', 'host', host)
    if user:
        cfg.set('Server', 'user', user)
    if name:
        cfg.set('Server', 'database', name)

    try:
        server = open_database(**dict(cfg.items('Server')))
    except Exception as e:
        raise click.ClickException(f"Cannot connect to server: {e}")

    server.__class__ = vault.Server
    ctx.obj = server


@seqvault.command()
@click.pass_obj
def listdb(server):
    """List databases.

    This command prints information about the databases available on the
    server.
    """

    print("NAME            PREFIX  ENTRIES")
    for db in server.values():
        print(f"{db.name:16}{db.get_prefix():8}{len(db)}")


@seqvault.command()
@click.argument('name')
@click.option('--prefix', '-p', help="The database prefix.")
@click.option('--description', '-d', help="A description of the database.")
@click.pass_obj
def newdb(server, name, prefix, description):
    """Create a new database.
    
    This command creates a new database on the server.
    """

    if not prefix:
        prefix = name[:3].upper()
    server.new_database(name, prefix, description)


@seqvault.command()
@click.argument('database', callback=_get_database)
@click.option('--output', '-o', metavar="USA", default='fasta::stdout',
              callback=_get_usa,
              help="Write to the specified USA instead of standard output.")
def export(database, output):
    """Export sequences from a database.

    This command exports all the sequences contained in the specified
    DATABASE.
    """

    output.write(database.get_unique_Seqs())


@seqvault.command('list')
@click.argument('database', callback=_get_database)
@click.option('--all', '-a', 'show_all', is_flag=True,
              help="Include obsolete sequences.")
def list_records(database, show_all):
    """List database contents.

    This command list all the sequences contained in the specified
    DATABASE.
    """

    if show_all:
        entries = database.values()
    else:
        entries = database.get_unique_seqs()
    for entry in entries:
        print(f"{entry.name:17}{entry.id:15}{entry.description}")


@seqvault.command()
@click.argument('accessions', nargs=-1)
@click.option('--output', '-o', metavar="USA", default='fasta::stdout',
              callback=_get_usa,
              help="Write to the specified USA instead of standard output.")
@click.pass_obj
def get(server, accessions, output):
    """Extract sequences from a database.

    This command extract sequences with the specified ACCESSIONS from
    any database on the server.
    """

    records = []
    for accession in accessions:
        records.append(server.get_Seq_by_accession(accession))
    if len(records) > 0:
        output.write(records)


@seqvault.command()
@click.argument('database', callback=_get_database)
@click.argument('sequences', nargs=-1, callback=_get_usas)
@click.pass_obj
def add(server, database, sequences):
    """Add sequences to a database.

    This command imports the specified SEQUENCES (as USAs) into the
    specified DATABASE.
    """

    try:
        records = []
        for usa in sequences:
            records.extend(usa.read())
    except Exception as e:
        raise click.ClickException(f"Cannot read sequences: {e}")

    try:
        database.load(records)
        server.commit()
    except Exception as e:
        raise click.ClickException(f"Cannot load sequences: {e}")

    # Extract newly inserted records and write them out
    extracted = []
    try:
        for record in records:
            rid = str(record.annotations['gi'])
            extracted.append(database.lookup(gi=rid))
        write_usa(extracted, 'genbank::stdout')
    except Exception as e:
        raise click.ClickException(f"Cannot write sequences: {e}")


@seqvault.command()
@click.argument('accession')
@click.option('--editor', '-e', default='/usr/bin/gvim --nofork',
              help="The editor command to use.")
@click.option('--read-only', '-r', is_flag=True,
              help="View the record only, do not store back any change.")
@click.pass_obj
def edit(server, accession, editor, read_only):
    """Edit a record.

    This command extracts the sequence with the specified ACCESSION
    number and fires up an external editor to view and edit the
    sequence before saving any changes back to the database.
    """

    record = server.get_Seq_by_accession(accession)

    tmpfile = NamedTemporaryFile(mode='w', delete=False)
    SeqIO.write(record, tmpfile, 'genbank')
    tmpfile.close()

    if not read_only:
        h1 = md5(open(tmpfile.name, 'rb').read()).hexdigest()

    command = editor.split()
    command.append(tmpfile.name)

    run(command)

    if not read_only:
        h2 = md5(open(tmpfile.name, 'rb').read()).hexdigest()
        if h1 != h2:
            new_record = SeqIO.read(tmpfile.name, 'genbank')
            if server.is_prefixed():
                db = server.get_database_by_prefix(new_record.id[:3])
            else:
                # If database prefixes are not supported, load the
                # record back into the same DB it was extracted from
                db = server.get_database_for_accession(accession)
            db.load([new_record])
            server.commit()

            extracted = db.lookup(gi=str(new_record.annotations['gi']))
            write_usa([extracted], 'genbank::stdout')


try:
    from IPython import embed

    @seqvault.command()
    @click.pass_obj
    def ipython(server):
        """Start a IPython shell.

        This command opens a connection to the BioSQL server then drops
        the user into a IPython shell.
        """

        embed()

except ImportError:
    pass

if __name__ == '__main__':
    try:
        seqvault()
    except Exception as e:
        print(f"seqvault: Unexpected error: {e}", file=sys.stderr)
