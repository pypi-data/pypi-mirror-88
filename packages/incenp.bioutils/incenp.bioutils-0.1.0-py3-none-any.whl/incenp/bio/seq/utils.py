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

"""Utility functions for working on biological sequences

This module is intended to provide various helper functions
for working on sequence files.
"""

from datetime import datetime
from random import sample

from Bio.Data import CodonTable
from Bio.Seq import MutableSeq, Seq
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio.SeqRecord import SeqRecord
from incenp.bio import Error

_reverse_codon_tables = {}


def _build_reverse_codon_table(code):
    rt = {}
    for residue in code.forward_table.values():
        codons_list = []
        for k, v in code.forward_table.items():
            if v == residue:
                codons_list.append(k)
        rt[residue] = codons_list
    return rt


def silently_mutate(sequence, code=None):
    """Mutate a CDS without changing its translation.
    
    Generate a mutated sequence by altering all possible codons
    without introducing any changes in the aminoacids translation.
    
    :param sequence: the sequence to mutate
    :type: :class:`Bio.Seq.Seq`
    :param code: the codon table to use (defaults to the “standard” genetic code)
    :type: :class:`Bio.Data.CodonTable`
    :return: the mutated sequence
    :rtype: :class:`Bio.Seq.Seq`
    """

    if not code:
        code = CodonTable.unambiguous_dna_by_name['Standard']
    if not code in _reverse_codon_tables:
        _reverse_codon_tables[code] = _build_reverse_codon_table(code)
    rt = _reverse_codon_tables[code]

    output = MutableSeq('')
    for i in range(int(len(sequence) / 3)):
        codon = str(sequence[i * 3:(i * 3) + 3])
        if codon in code.forward_table:
            residue = code.forward_table[codon]
            possible_codons = rt[residue]
            if len(possible_codons) > 1:
                codon = sample([a for a in possible_codons if a != codon], 1)[0]
        output += codon

    return output


def genbank_date(date=None):
    if date is None:
        date = datetime.now()
    return date.strftime('%d-%b-%Y').upper()


def remove_external_features(record):
    for feature in [f for f in record.features[:] if f.ref is not None]:
        record.features.remove(feature)


def clean(record, div='UNK', topology='linear'):
    # Set the data division if needed
    if (not 'data_file_division' in record.annotations
        or record.annotations['data_file_division'].isspace()):
        record.annotations['data_file_division'] = div

    # Fix topology
    if not 'topology' in record.annotations:
        record.annotations['topology'] = topology

    # Fix missing molecule type
    if not 'molecule_type' in record.annotations:
        record.annotations['molecule_type'] = guess_molecule_type(record.seq)

    # Translate CDS
    for cds in [f for f in record.features if f.type == 'CDS']:
        if 'translation' in cds.qualifiers:
            continue
        if record.annotations['molecule_type'] == 'protein':
            continue
        seq = record.seq[cds.location.start.position:cds.location.end.position]
        if cds.strand == -1:
            seq = seq.reverse_complement()
        cds.qualifiers['translation'] = str(seq.translate())

    # Remove Ugene stuff
    for feature in [f for f in record.features[:] if 'ugene_name' in f.qualifiers]:
        # Restriction site features
        if 'cut' in feature.qualifiers:
            record.features.remove(feature)

        # Fragments
        if 'ugene_group' in feature.qualifiers and 'fragments' in feature.qualifiers['ugene_group']:
            record.features.remove(feature)

        # Source
        if 'source' in feature.qualifiers['ugene_name']:
            record.features.remove(feature)

        feature.qualifiers.pop('ugene_name', None)
        feature.qualifiers.pop('ugene_group', None)

    # Remove SerialCloner stuff
    for feature in record.features:
        feature.qualifiers.pop('SerialCloner_Color', None)
        feature.qualifiers.pop('SerialCloner_Show', None)
        feature.qualifiers.pop('SerialCloner_Protect', None)
        feature.qualifiers.pop('SerialCloner_Arrow', None)


_alphabets = {
    'DNA': 'ACGTRYSWKMBDHVN',
    'RNA': 'ACGURYSWKMBDHVN',
    'protein': 'ACDEFGHIKLMNPQRSTVWY*'
    }


def guess_molecule_type(sequence, alphabets=_alphabets):
    seqset = set(str(sequence).upper())
    for typename in alphabets.keys():
        leftover = seqset - set(alphabets[typename])
        if not leftover:
            return typename
    return 'DNA'


_gateway_sequences = {
        'attB1': 'ACAAGTTTGTACAAAAAAGCAGGCT',
        'attB2': 'ACCCAGCTTTCTTGTACAAAGTGGT',
        'attL1': 'AAATAATGATTTTATTTTGACTGATAGTGACCTGTTCGTTGCAACACATTGATGAGCAAT'
                 'GCTTTTTTATAATGCCAACTTTGTACAAAAAAGCAGGCT',
        'attL2': 'ACCCAGCTTTCTTGTACAAAGTTGGCATTATAAGAAAGCATTGCTTATCAATTTGTTGCA'
                 'ACGAACAGGTCACTATCAGTCAAAATAAAATCATTATTT',
        'attP1': 'AAATAATGATTTTATTTTGACTGATAGTGACCTGTTCGTTGCAACACATTGATGAGCAAT'
                 'GCTTTTTTATAATGCCAACTTTGTACAAAAAAGCTGAACGAGAAACGTAAAATGATATAA'
                 'ATATCAATATATTAAATTAGATTTTGCATAAAAAACAGACTACATAATACTGTAAAACAC'
                 'AACATATCCAGTCACTATGAATCAACTACTTAGATGGTATTAGTGACCTGTA',
        'attP2': 'TACAGGTCACTAATACCATCTAAGTAGTTGATTCATAGTGACTGGATATGTTGTGTTTTA'
                 'CAGTATTATGTAGTCTGTTTTTTATGCAAAATCTAATTTAATATATTGATATTTATATCA'
                 'TTTTACGTTTCTCGTTCAGCTTTCTTGTACAAAGTTGGCATTATAAGAAAGCATTGCTTA'
                 'TCAATTTGTTGCAACGAACAGGTCACTATCAGTCAAAATAAAATCATTATTT',
        'attR1': 'ACAAGTTTGTACAAAAAAGCTGAACGAGAAACGTAAAATGATATAAATATCAATATATTA'
                 'AATTAGATTTTGCATAAAAAACAGACTACATAATACTGTAAAACACAACATATCCAGTCA'
                 'CTATG',
        'attR2': 'ATAGTGACTGGATATGTTGTGTTTTACAGTATTATGTAGTCTGTTTTTTATGCAAAATCT'
                 'AATTTAATATATTGATATTTATATCATTTTACGTTTCTCGTTCAGCTTTCTTGTACAAAG'
                 'TGGT'
        }

_gateway_reactions = {
        'BP': {
                'source': ['attB1', 'attB2'],
                'target': ['attP1', 'attP2'],
                'result': ['attL1', 'attL2']
                },
        'LR': {
                'source': ['attL1', 'attL2'],
                'target': ['attR1', 'attR2'],
                'result': ['attB1', 'attB2']
                }
        }


def _find_gateway_sites(sequence, reaction='LR', kind='source', log=None):
    indexes = []
    for i in [0, 1]:
        name = _gateway_reactions[reaction][kind][i]
        seq = _gateway_sequences[name]
        index = sequence.seq.find(seq)
        if index == -1:
            if log:
                log.write("No {} site found in {} sequence\n".format(name, kind))
            continue
        if (kind == 'source' and i == 0) or (kind == 'target' and i == 1):
            index += len(seq)
        indexes.append(index)
    return indexes


def gateway(source, destination, reaction='LR', log=None):
    """Perform a Gateway reaction between two sequences.
    
    :param source: the source sequence
    :type: :class:`Bio.Seq.SeqRecord`
    :param destination: the destination sequence
    :type: :class:`Bio.Seq.SeqRecord`
    :param reaction: the type of Gateway reaction to perform ('LR' or 'BP')
    :type: str
    :param log: a file-like object to write debug informations to
    :return: the destination product of the Gateway reaction, or None
             if no reaction was possible
    :rtype: :class:`Bio.Seq.SeqRecord`
    """

    if reaction not in _gateway_reactions:
        raise Error("Invalid Gateway reaction type: {}".format(reaction))

    src_indexes = _find_gateway_sites(source, reaction, 'source', log)
    if len(src_indexes) != 2:
        return
    source_part = source[src_indexes[0]:src_indexes[1]]
    if log:
        log.write("Found source region: {}..{}\n".format(src_indexes[0], src_indexes[1]))

    dst_indexes = _find_gateway_sites(destination, reaction, 'target', log)
    if len(dst_indexes) != 2:
        return
    dest_parts = [destination[:dst_indexes[0]], destination[dst_indexes[1]:]]
    if log:
        log.write("Found target region: {}..{}\n".format(dst_indexes[0], dst_indexes[1]))

    result_sites = []
    for i in [0, 1]:
        name = _gateway_reactions[reaction]['result'][i]
        seq = _gateway_sequences[name]
        rec = SeqRecord(Seq(seq))
        strand = 1
        if i == 1:
            strand = -1
        rec.features.append(
                SeqFeature(FeatureLocation(0, len(seq), strand=strand),
                           type='misc_recomb',
                           qualifiers={'note': [name + ' recombination site']}))
        result_sites.append(rec)

    clone = dest_parts[0] + result_sites[0] + source_part + result_sites[1] + dest_parts[1]

    return clone
