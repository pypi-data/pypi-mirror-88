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

"""An implementation of EMBOSS Uniform Sequence address.

Uniform Sequence Addresses (USAs) are a way to refer to a sequence by
specifying the file the sequence is to be read from or the database it
is to be fetched from, as well as other informations such as the
expected format.

USAs are described in EMBOSS documentation:
<http://emboss.sourceforge.net/docs/themes/UniformSequenceAddress.html>.
"""

import re
import sys
from os.path import splitext

from Bio.Seq import Seq
from Bio.SeqIO import parse, write
from Bio.SeqRecord import SeqRecord

from incenp.bio import Error

_range_spec = re.compile('^([^]]+)\[(-?\d+)?:(-?\d+)?(:r)?\]$')

_search_fields = [
    'acc',
    'des',
    'id',
    'key',
    'org',
    'sv'
    ]


class FragmentSpec:
    """Represents a sequence fragment specification."""

    def __init__(self, start, end, reverse):
        self.start = start
        self.end = end
        self.reverse = reverse


class USA:
    """Represents a parsed Uniform Sequence Address."""

    def __init__(self, fmt=None, fragment=None):
        self.format = fmt
        self.fragment = fragment

    def read(self):
        """Get the sequence records referred to by this USA.
        
        :return: the sequence records
        :rtype: list(:class:`Seq.SeqRecord.SeqRecord`)
        """

        records = self._do_read()
        if self.fragment is not None:
            records = [self._truncate(r, self.fragment) for r in records]
        return records

    def write(self, records):
        """Write sequence records to the backend referred to by this USA.
        
        :param records: the sequence records to write
        :type: list(:class:`Seq.SeqRecord.SeqRecord`)
        """

        raise Error("Writing to this type of USA is not supported")

    def _do_read(self):
        raise Error("Fetching records from this USA is not supported")

    def _truncate(self, record, fragment):
        start = fragment.start
        if start is not None and start > 0:
            start -= 1
        end = fragment.end
        if end is not None and end < 0:
            end += 1
        new = record[start:end]
        if fragment.reverse:
            new = new.reverse_complement()
        return new


class ListUSA(USA):
    """Represents a USA that is itself a list of USAs."""

    def __init__(self, usas):
        super(ListUSA, self).__init__()
        self.usas = usas

    def _do_read(self):
        records = []
        for usa in self.usas:
            records.extend(usa.read())
        return records


class FileUSA(USA):
    """Represents a USA referring to sequences in a file."""

    def __init__(self, filename, identifier=None, field=None, keyword=None):
        super(FileUSA, self).__init__()
        self.filename = filename
        self.identifier = identifier
        self.field = field
        self.keyword = keyword

    def _do_read(self):
        records = []
        for record in parse(self.filename, self.format):
            # TODO: Support wildcard identifiers
            # TODO: Support field-based searches
            if self.identifier is None or record.id == self.identifier:
                records.append(record)

        return records

    def write(self, records):
        output = sys.stdout if self.filename == 'stdout' else self.filename
        write(records, output, self.format)


class ProgramUSA(USA):
    """Represents a USA referring to sequences coming from a program."""

    def __init__(self, program, args):
        super(ProgramUSA, self).__init__()
        self.program = program
        self.args = args


class DatabaseUSA(USA):
    """Represents a USA referring to sequences in a database."""

    def __init__(self, database, identifier=None, field=None, keyword=None):
        super(DatabaseUSA, self).__init__()
        self.database = database
        self.identifier = identifier
        self.field = field
        self.keyword = keyword


class AsisUSA(USA):
    """Represents a USA containing an inline sequence."""

    def __init__(self, sequence):
        super(AsisUSA, self).__init__('asis')
        self.sequence = sequence

    def _do_read(self):
        return [SeqRecord(Seq(self.sequence))]


def _parse_list(usa, databases=None, fmt=None, fragment=None):
    if usa.startswith('@'):
        usa = usa[1:]
    elif usa.startswith('list:'):
        usa = usa[5:]
    else:
        return False

    usas = []
    with open(usa, 'r') as f:
        for line in f:
            line = line.strip()
            if line == '' or line[0] == '#':
                continue
            usas.append(parse_usa(line, databases, fmt, fragment))
    return ListUSA(usas)


def _parse_program(usa):
    if usa[-1] != '|':
        return False

    parts = usa[:-1].split()
    return ProgramUSA(parts[0], parts[1:])


def _parse_database(usa, databases=None):
    parts = usa.split(':')
    dbname = parts[0]
    dbfield = None
    if '-' in dbname:
        dbname, dbfield = dbname.split('-', maxsplit=1)
    if dbname not in databases:
        return False

    if len(parts) == 1:
        if dbfield is not None:
            raise Error("Invalid database USA: keyword required")
        return DatabaseUSA(dbname)
    elif len(parts) == 2:
        if dbfield is not None:
            return DatabaseUSA(dbname, field=dbfield, keyword=parts[1])
        else:
            return DatabaseUSA(dbname, identifier=parts[1])
    else:
        raise Error("Invalid database USA: too many parts")


_format_extensions = {
    '.gb': 'genbank',
    '.fasta': 'fasta',
    '.fas': 'fasta',
    '.xdna': 'xdna',
    '.dna': 'snapgene',
    '.ab1': 'abi',
    '.gck': 'gck'
    }


def _parse_file(usa, guess_format=False, extensions_map={}):
    parts = usa.split(':')
    filename = parts[0]

    if len(parts) == 1:
        ret = FileUSA(filename)
    elif len(parts) == 2:
        ret = FileUSA(filename, identifier=parts[1])
    elif len(parts) == 3:
        ret = FileUSA(filename, field=parts[1], keyword=parts[2])
    else:
        raise Error("Invalid file USA: too many parts")

    if guess_format:
        _, ext = splitext(filename.lower())
        if ext and ext in extensions_map:
            ret.format = extensions_map[ext]

    return ret


def parse_usa(usa, databases=[], fmt='fasta', fragment=None,
              extensions_map=_format_extensions):
    """Parses a Uniform Sequence Address into a compiled form.
    
    :param usa: the Uniform Sequence Address to parse
    :type: str
    :param databases: valid database names
    :type: list(str)
    :return: the compiled form of the input USA
    :rtype: :class:`incenp.bio.seq.usa.USA`
    """

    compiled = False
    explicit_fmt = False

    if '::' in usa:
        fmt, usa = usa.split('::', 1)
        explicit_fmt = True

    m = _range_spec.match(usa)
    if m:
        usa = m.group(1)
        start = int(m.group(2)) if m.group(2) is not None else None
        end = int(m.group(3)) if m.group(3) is not None else None
        reverse = True if m.group(4) is not None else None
        if fragment is not None:
            if start is None and fragment.start is not None:
                start = fragment.start
            if end is None and fragment.end is not None:
                end = fragment.end
            if reverse is None and fragment.reverse is not None:
                reverse = fragment.reverse
        fragment = FragmentSpec(start, end, reverse)

    if fmt == 'asis':
        compiled = AsisUSA(usa)

    if not compiled:
        compiled = _parse_list(usa, databases, fmt, fragment)

    if not compiled:
        compiled = _parse_program(usa)

    if not compiled:
        compiled = _parse_database(usa, databases)

    if not compiled:
        compiled = _parse_file(usa, not explicit_fmt, extensions_map)

    if not compiled:
        # Should never happen
        raise Error("Unrecognized USA type")

    if compiled.format is None:
        compiled.format = fmt
    if fragment is not None and not isinstance(compiled, ListUSA):
        compiled.fragment = fragment

    return compiled


def read_usa(usa):
    """Read sequences referred to by a USA.
    
    This function parses the provided USA and then fetches the corresponding
    sequences.
    
    :param usa: the Uniform Sequence Address
    :type: str
    :return: the corresponding sequence records
    :rtype: list(:class:`Bio.SeqRecord.SeqRecord`)
    """

    compiled = parse_usa(usa)
    records = compiled.read()
    return records


def write_usa(records, usa):
    """Write sequence records to a USA.
    
    :param records: the sequence records to write
    :type: list(:class:`Bio.SeqRecord.SeqRecord`)
    :param usa: the Uniform Sequence Address
    :type: str
    """

    compiled = parse_usa(usa)
    compiled.write(records)
