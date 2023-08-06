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

"""Graphical description of plasmids."""

from Bio.Graphics import GenomeDiagram
from Bio.Restriction import Analysis, RestrictionBatch
from Bio.SeqFeature import SeqFeature, FeatureLocation
from reportlab.lib import colors, pagesizes


def _get_feature_label(feature):
    label = None

    if 'label' in feature.qualifiers:
        label = feature.qualifiers['label'][0]
    elif 'gene' in feature.qualifiers:
        label = feature.qualifiers['gene'][0]
        if 'function' in feature.qualifiers:
            label += " (%s)" % feature.qualifiers['function'][0]
        elif 'product' in feature.qualifiers:
            label += " (%s)" % feature.qualifiers['product'][0]
    elif 'note' in feature.qualifiers:
        label = feature.qualifiers['note'][0]
    elif feature.type == 'primer_bind':
        label = "primer"

    return label


_page_width, _page_height = pagesizes.A4
_page_margin = 30
_text_width = _page_width - 2 * _page_margin
_text_vert_offset = _page_height - 30

# Arbitrary selection of default enzymes
_enzymes = RestrictionBatch(['AflII', 'ApaBI', 'ApaLI', 'AscI', 'AvaI',
                             'BamHI', 'BglII', 'BstBI',
                             'ClaI',
                             'EcoRI', 'EcoRV',
                             'HindIII',
                             'KpnI',
                             'MluI',
                             'NcoI', 'NdeI', 'NheI', 'NotI',
                             'PstI', 'PvuI', 'PvuII',
                             'SacI', 'SacII', 'SalI', 'ScaI', 'SnaBI', 'SpeI',
                             'XbaI', 'XhoI'])


def generate_map(vector, size=(500, 500)):
    """Create a circular map from a plasmid sequence.
    
    :param vector: the annotated plasmid sequence
    :type: :class:`Bio.Seq.SeqRecord`
    :param size: the size of the map to generate
    :type: (int, int)
    :return: the generated map
    """

    diagram = GenomeDiagram.Diagram(vector.seq)
    diagram.start = 0
    diagram.end = len(vector) + 1
    diagram.pagesize = size

    seq_track = diagram.new_track(3, name='Sequence')
    seq_track.scale = True
    seq_track.scale_ticks = True
    seq_track.scale_largetick_interval = len(vector)
    seq_track.scale_largetick_labels = True
    seq_track.scale_smalltick_interval = 500
    seq_track.scale_smalltick_labels = True
    seq_track.height = 0.6

    feat_track = diagram.new_track(3, name='Features')
    feat_track.scale = False
    feat_track.height = 1

    cds_set = feat_track.new_set()
    primer_set = seq_track.new_set()

    for feat in vector.features:
        if feat.strand == None:
            feat.strand = 1

        if feat.type == 'CDS':
            cds_set.add_feature(feat, label=True, sigil='ARROW',
                                color=colors.green, label_size=8)
        elif feat.type in ('promoter', 'LTR'):
            cds_set.add_feature(feat, sigil='ARROW', color=colors.lightgreen)
        elif feat.type == 'primer_bind':
            primer_set.add_feature(feat, name="primer", label=True,
                                   color=colors.lightblue, label_size=4,
                                   sigil='ARROW')

    rest_track = diagram.new_track(4, name='Enzymes')
    rest_track.scale = False
    rest_track.height = 0.8
    rest_set = rest_track.new_set()

    all_sites = Analysis(_enzymes, vector.seq, linear=False).with_N_sites(1)
    for enzyme in all_sites.keys():
        name = "%s" % enzyme
        pos = all_sites[enzyme][0]
        feat = SeqFeature(FeatureLocation(pos, pos), strand=1)
        rest_set.add_feature(feat, name=name, label=True, color=colors.red)

    diagram.draw(format='circular', circular=True)
    return diagram.drawing


def summarize_vector(canvas, vector):
    """Create a report describing a plasmid.
    
    :param canvas: the canvas where the report is to be drawn on
    :type: :class:`reportlib.pdfgen.canvas.Canvas`
    :param vector: the annotated plasmid sequence
    :type: :class:`Bio.Seq.SeqRecord`
    """

    hdr = canvas.beginText(_page_margin, _text_vert_offset)
    hdr.setFont('Helvetica', 12)
    hdr.textLine("The {} plasmid ({})".format(vector.name, vector.id))
    hdr.setFont('Helvetica-Oblique', 8)
    hdr.textLine(vector.description)
    if 'comment' in vector.annotations:
        hdr.textLines(vector.annotations['comment'])
    canvas.drawText(hdr)
    canvas.line(_page_margin, hdr.getY(), _text_width, hdr.getY())

    vmap = generate_map(vector, size=(_text_width, _text_width))
    vmap.drawOn(canvas, _page_margin, hdr.getY() - vmap.height)

    flist = canvas.beginText(_page_margin, hdr.getY() - vmap.height)
    flist.setFont('Courier', 8)
    for feat in vector.features:
        strand = '+'
        if feat.strand == -1:
            strand = '-'
        label = _get_feature_label(feat)
        flist.textLine("%d-%d (%s) [%s] %s" % (
                feat.location.start + 1, feat.location.end, strand,
                feat.type, label
                ))
    canvas.drawText(flist)

    canvas.showPage()
