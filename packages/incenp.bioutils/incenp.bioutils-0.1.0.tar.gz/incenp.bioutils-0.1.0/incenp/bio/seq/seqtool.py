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
"""A command-line tool to manipulate biological sequence files."""

import sys

from Bio.Restriction.Restriction import RestrictionBatch
import click
from incenp.bio import __version__
from incenp.bio.seq import utils
from incenp.bio.seq import wrappers
from incenp.bio.seq.plasmidmap import summarize_vector
from incenp.bio.seq.usa import read_usa, write_usa

try:
    from reportlab.pdfgen.canvas import Canvas
except ImportError:
    pass

prog_name = "seqtool"
prog_notice = f"""\
{prog_name} {__version__}
Copyright © 2020 Damien Goutte-Gattat

This program is released under the GNU General Public License.
See the COPYING file or <http://www.gnu.org/licenses/gpl.html>.
"""


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version=__version__, message=prog_notice)
@click.pass_context
def seqtool(ctx):
    pass


@seqtool.command()
@click.argument('sequences', nargs=-1)
@click.option('--output', '-o', default='genbank::stdout', metavar="USA",
              help="""Write to the specified USA instead of standard
                      output.""")
@click.option('--name', '-n', metavar="NAME", help="Set the sequence name.")
@click.option('--accession', '-a', metavar="ACC", help="Set the sequence ID.")
@click.option('--description', '-d', help="Set the sequence description.")
@click.option('--circular', '-c', 'topology', flag_value='circular',
              help="Force circular topology.")
@click.option('--linear', 'topology', flag_value='linear', default=True,
              help="Force linear topology.")
@click.option('--division', '-D', metavar="DIV",
              help="""The data file division to use if none is already
                      assigned to the sequence.""")
@click.option('--clean', '-C', is_flag=True,
              help="Clean the output sequence.")
@click.option('--remove-external-features', '-r', is_flag=True,
              help="Remove features referring to an external sequence.")
@click.pass_context
def cat(ctx, sequences, output, name, accession, description, topology,
        division, clean, remove_external_features):
    """Read and write sequences.
    
    This tool reads the specified input SEQUENCES and catenate them into
    a single written to standard output.
    """

    inputs = []
    for f in sequences:
        try:
            inputs.extend(read_usa(f))
        except Exception as e:
            raise click.ClickException(f"Cannot read {f}: {e}")

    if len(inputs) == 0:
        ctx.exit()

    outrec = inputs[0]
    for record in inputs[1:]:
        outrec += record

    if clean:
        utils.clean(outrec, div=division, topology=topology)
    if remove_external_features:
        utils.remove_external_features(outrec)
    if name:
        outrec.name = name
    if accession:
        outrec.id = accession
    if description:
        outrec.description = description

    try:
        write_usa([outrec], output)
    except Exception as e:
        raise click.ClickException(f"Cannot write to {output}: {e}")


@seqtool.command()
@click.argument('source')
@click.option('--output', '-o', metavar="USA", default='fasta::stdout',
              help="""Write to the specified USA instead of standard
                      output.""")
@click.pass_context
def siresist(ctx, source, output):
    """Silently mutate a CDS.
    
    Creates a variant of the SOURCE sequence with silent mutations.
    """

    try:
        source = read_usa(source)[0]
    except Exception as e:
        raise click.ClickException(f"Cannot read {source}: {e}")

    source.seq = utils.silently_mutate(source.seq)

    try:
        write_usa([source], output)
    except Exception as e:
        raise click.ClickException(f"Cannot write to {output}: {e}")


@seqtool.command()
@click.argument('source')
@click.argument('destination')
@click.option('--output', '-o', metavar="USA",
              help="""Write to the specified USA instead of standard
                      output.""")
@click.option('--reaction', '-r', type=click.Choice(['BP', 'LR']),
              default='LR',
              help="Specify the type of Gateway reaction.")
@click.option('--name', '-n', metavar="NAME", help="Set the sequence name.")
@click.option('--accession', '-a', metavar="ACC", help="Set the sequence ID.")
@click.option('--description', '-d', help="Set the sequence description.")
@click.option('--clean', '-c', is_flag=True, help="Clean the output sequence.")
@click.pass_context
def gateway(ctx, source, destination, output, reaction, name, accession,
            description, clean):
    """Perform in-silico Gateway cloning."""

    try:
        source = read_usa(source)[0]
        destination = read_usa(destination)[0]
    except Exception as e:
        raise click.ClickException(f"Cannot read input sequences: {e}")

    clone = utils.gateway(source, destination, reaction, sys.stderr)
    if not clone:
        raise click.ClickException("Gateway cloning not possible")

    clone.name = name or source.name
    clone.id = accession or source.id
    clone.description = description or source.description
    clone.annotations['date'] = utils.genbank_date()

    if clean:
        utils.clean(clone)

    try:
        write_usa([clone], output)
    except Exception as e:
        raise click.ClickException(f"Cannot write output: {e}")


@seqtool.command()
@click.argument('sequences', nargs=-1)
@click.option('--output', '-o', metavar="FILE", default='plasmm.pdf',
              help="Write to the specified file.", show_default=True)
@click.option('--enzymes', '-e', help="Specify the enzymes to display.")
@click.pass_context
def plasmm(ctx, sequences, output, enzymes):
    """Draw plasmid maps."""

    if enzymes:
        _enzymes = RestrictionBatch()
        for enz in enzymes.split(','):
            _enzymes.add(enz)

    records = []
    for f in sequences:
        try:
            records.extend(read_usa(f))
        except Exception as e:
            raise click.ClickException(f"Cannot read {f}: {e}")

    c = Canvas(output)
    for record in records:
        if record.annotations.get('molecule_type', 'DNA') == 'protein':
            continue
        summarize_vector(c, record)

    try:
        c.save()
    except Exception as e:
        raise click.ClickException(f"Cannot write output: {e}")


@seqtool.command()
@click.argument('subject')
@click.argument('query')
@click.option('--type', '-t', 'blast_type', default='blastn',
              type=click.Choice(['blastn', 'blastp', 'blastx', 'tblastn',
                                 'tblastx']),
              help="The type of alignment to perform.")
@click.option('--database', '-d', is_flag=True,
              help="Treat SUBJECT as a database name.")
@click.option('--short', '-s', is_flag=True,
              help="Optimize BLAST for short matches.")
def blast(ctx, subject, query, blast_type, database, short):
    """Wrapper for the BLAST programs.
    
    SUBJECT and QUERY should be USAs representing the subject and query
    sequences, respectively.
    """

    try:
        if not database:
            subject = read_usa(subject)[0]
        query = read_usa(query)[0]
    except Exception as e:
        raise click.ClickException(f"Cannot read source sequences: {e}")

    try:
        stdout, _ = wrappers.blast(query, subject, blast_type, database, short)
        print(stdout)
    except BrokenPipeError:
        pass
    except Exception as e:
        raise click.ClickException(f"Cannot run blast: {e}")


@seqtool.command()
@click.argument('hseq')
@click.argument('vseq')
@click.pass_context
def dotter(ctx, hseq, vseq):
    """Wrapper for the dotter program."""

    try:
        hseq = read_usa(hseq)[0]
        vseq = read_usa(vseq)[0]
    except Exception as e:
        raise click.ClickException(f"Cannot read source sequences: {e}")

    try:
        wrappers.dotter(hseq, vseq)
    except Exception as e:
        raise click.ClickException(f"Cannot run dotter: {e}")


if __name__ == '__main__':
    seqtool()
