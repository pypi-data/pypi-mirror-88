# -*- coding: utf-8 -*-
# Incenp.Bioutils - Incenp.org's utilities for computational biology
# Copyright © 2018,2020 Damien Goutte-Gattat
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

"""Wrappers for external programs

This module provides wrapper functions to call third-party sequence
manipulation tools.
"""

from os import unlink
from subprocess import call
from tempfile import NamedTemporaryFile

from Bio.Blast import Applications
from Bio.SeqIO import write

_applications = {
    'blastn': Applications.NcbiblastnCommandline,
    'blastp': Applications.NcbiblastpCommandline,
    'blastx': Applications.NcbiblastxCommandline,
    'tblastn': Applications.NcbitblastnCommandline,
    'tblastx': Applications.NcbitblastxCommandline
        }


def blast(query, subject, kind='blastn', is_database=False, short=False):
    """Call a BLAST program.
    
    :param query: the query sequence to blast for
    :type: :class:`Bio.Seq.SeqRecord`
    :param subject: the subject sequence or database to blast against
    :type: :class:`Bio.Seq.SeqRecord`, or str if is_database is True
    :param kind: the type of BLAST alignment to perform
    :type: str
    :param is_database: if True, treat subject as the name of a BLAST database
    :type: bool
    :param short: if True, blast for short sequences
    :type: bool
    :return: the outputs of the BLAST command
    :type: (str, str)
    """

    sf = None
    qf = None
    params = {}

    try:
        if not is_database:
            sf = NamedTemporaryFile(mode='w', delete=False)
            write([subject], sf, 'fasta')
            sf.close()
            params['subject'] = sf.name
        else:
            params['db'] = subject

        qf = NamedTemporaryFile(mode='w', delete=False)
        write([query], qf, 'fasta')
        qf.close()
        params['query'] = qf.name

        if short:
            params['task'] = kind + '-short'

        cmd = _applications[kind](**params)
        return cmd()

    finally:
        if not is_database and sf is not None:
            unlink(sf.name)
        if qf is not None:
            unlink(qf.name)


def dotter(horizontal, vertical):
    """Call the dotter program on the specified sequences.
    
    :param horizontal: the sequence to plot on the horizontal axis
    :type: :class:`Bio.SeqRecord.SeqRecord`
    :param vertical: the sequence to plot on the vertical axis
    :type: :class:`Bio.SeqRecord.SeqRecord`
    """

    try:
        hf = NamedTemporaryFile(mode='w', delete=False)
        vf = NamedTemporaryFile(mode='w', delete=False)

        write([horizontal], hf, 'fasta')
        hf.close()

        write([vertical], vf, 'fasta')
        vf.close()

        call(['dotter', hf.name, vf.name])
    finally:
        unlink(hf.name)
        unlink(vf.name)
