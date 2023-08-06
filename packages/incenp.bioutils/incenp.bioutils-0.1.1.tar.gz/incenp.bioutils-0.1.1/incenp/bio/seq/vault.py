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

"""Access a BioSQL-based sequence vault."""

from BioSQL.BioSeq import DBSeqRecord
from BioSQL.BioSeqDatabase import BioSeqDatabase, DBServer
from BioSQL.Loader import DatabaseLoader


class Server(DBServer):

    def __getitem__(self, name):
        """Get the specified sub-database."""

        return Database(self.adaptor, name, self.is_prefixed())

    def new_database(self, db_name, prefix, description=None):
        """Create a new sub-database."""

        if self.is_prefixed():
            sql = (
                'INSERT INTO biodatabase (name, prefix, description) '
                'VALUES (%s, %s, %s)'
                )
            self.adaptor.execute(sql, (db_name, prefix, description))
        else:
            sql = (
                'INSERT INTO biodatabase (name, description'
                'VALUES (%s, %s'
                )
            self.adaptor.execute(sql, (db_name, description))
        return Database(self.adaptor, db_name, self.is_prefixed())

    def get_database_by_prefix(self, prefix):
        """Get the database that uses the specified prefix."""

        if not self.is_prefixed():
            return None

        sql = (
            'SELECT name FROM biodatabase '
            'WHERE prefix = %s'
            )
        res = self.adaptor.execute_one(sql, (prefix,))
        if res:
            return Database(self.adaptor, res, True)
        else:
            return None

    def get_database_for_accession(self, name):
        """Get the database containing a given accession number."""

        acc, _, version = name.partition('.')
        if version:
            sql = (
                'SELECT name FROM biodatabase WHERE biodatabase_id IN '
                '(SELECT biodatabase_id FROM bioentry '
                ' WHERE accession = %s AND VERSION = %s)'
                )
            res = self.adaptor.execute_one(sql, (acc, version))
        else:
            sql = (
                'SELECT name FROM biodatabase WHERE biodatabase_id IN '
                '(SELECT biodatabase_id FROM bioentry '
                ' WHERE accession = %s)'
                )
            res = self.adaptor.execute_one(sql, (acc,))
        if not res:
            raise Exception(f"No database found for accession {name}")
        return Database(self.adaptor, res, self.is_prefixed())

    def is_prefixed(self):
        """Indicate whether the server supports prefixed databases.
        
        This method returns true if the server uses a modified BioSQL
        schema where biodatabases are associated with a prefix to use
        in accession numbers.
        """

        try:
            return self._is_prefixed
        except AttributeError:
            self.adaptor.execute('SELECT * FROM biodatabase LIMIT 1')
            columns = [desc.name for desc in self.adaptor.cursor.description]
            self._is_prefixed = 'prefix' in columns
            return self._is_prefixed

    def get_Seq_by_accession(self, name):
        """Get a sequence from any sub-database."""

        acc, _, version = name.partition('.')
        if version:
            sql = (
                'SELECT bioentry_id FROM bioentry '
                'WHERE accession = %s '
                'AND version = %s'
                )
            res = self.adaptor.execute_and_fetchall(sql, (acc, version))
        else:
            sql = (
                'SELECT bioentry_id FROM bioentry '
                'WHERE accession = %s '
                'ORDER BY version DESC LIMIT 1'
                )
            res = self.adaptor.execute_and_fetchall(sql, (acc,))
        if not res:
            raise Exception("no record found for accession {}".format(name))
        return DBSeqRecord(self.adaptor, res[0][0])


class Database(BioSeqDatabase):

    def __init__(self, adaptor, name, prefixed=True):
        BioSeqDatabase.__init__(self, adaptor, name)
        self._is_prefixed = prefixed

    def get_prefix(self):
        """Get the database prefix."""

        if not self._is_prefixed:
            return ''

        sql = (
            'SELECT prefix FROM biodatabase '
            'WHERE biodatabase_id = %s'
            )
        return self.adaptor.execute_one(sql, (self.dbid,))[0]

    def get_unique_seqs(self):
        sql = 'SELECT max(bioentry_id) FROM bioentry ' \
              'WHERE biodatabase_id = %s ' \
              'GROUP BY accession ORDER BY accession'
        res = self.adaptor.execute_and_fetchall(sql, (self.dbid,))
        return [DBSeqRecord(self.adaptor, eid) for eid in res]

    def get_Seq_by_unversioned_acc(self, name):
        """Get the most recent version of a record by accession number."""

        seqids = self.adaptor.fetch_seqids_by_accession(self.dbid, name)
        if not seqids:
            return None
        return DBSeqRecord(self.adaptor, seqids[-1])

    def get_Seq_by_accession(self, name):
        """Get the record identified by the specified accession number.
        
        This method does The Right Thing: if the specified accession number
        is versioned, it returns the exact requested version; if the
        accession number is not versioned, it returns the most recent
        version."""

        acc, _, version = name.partition('.')
        if version:
            return self.get_Seq_by_ver(name)
        else:
            return self.get_Seq_by_unversioned_acc(acc)

    def _get_last_id(self):
        """Get the largest GI identifier used so far."""

        sql = (
            'SELECT identifier FROM bioentry '
            'ORDER BY CAST(identifier AS int) DESC LIMIT 1'
            )
        res = self.adaptor.execute_and_fetchall(sql)
        if res:
            return int(res[0][0])
        else:
            return 0

    def _get_last_accession(self):
        """Get the largest accession number used so far."""

        sql = (
            'SELECT accession FROM bioentry '
            'WHERE biodatabase_id = %s '
            'ORDER BY accession DESC LIMIT 1'
            )
        res = self.adaptor.execute_and_fetchall(sql, (self.dbid,))
        if res:
            acc = res[0][0]
            return int(acc[4:])
        else:
            return 0

    def _get_last_version_for_accession(self, acc):
        """Get the largest version for the specified record."""

        sql = (
            'SELECT version FROM bioentry '
            'WHERE biodatabase_id = %s AND accession = %s '
            'ORDER BY version DESC LIMIT 1'
            )
        res = self.adaptor.execute_and_fetchall(sql, (self.dbid, acc))
        if res:
            return res[0][0]
        else:
            return 0

    def load(self, record_iterator, fetch_NCBI_taxonomy=False):
        """Load a set of SeqRecords into the database."""

        if not self._is_prefixed:
            # If prefixes are not supported, we don't mangle the GI and
            # accession numbers. It is then up to the caller to provide
            # correct GI and accession numbers.
            return BioSeqDatabase.load(record_iterator, fetch_NCBI_taxonomy)

        prefix = self.get_prefix()
        last_id = self._get_last_id()
        last_acc = self._get_last_accession()
        num_records = 0

        db_loader = DatabaseLoader(self.adaptor, self.dbid, fetch_NCBI_taxonomy)

        for record in record_iterator:
            num_records += 1

            # Force a newly generated identifier
            last_id += 1
            record.annotations['gi'] = last_id

            if record.name == record.id:
                # No accession in the record, generate one
                last_acc += 1
                record.id = '{}_{:06d}.1'.format(prefix, last_acc)
            else:
                # An accession number is provided, check the version
                acc, _, _ = record.id.partition('.')
                last_version = self._get_last_version_for_accession(acc)
                if last_version > 0:
                    # The accession number already exists, that's an update
                    record.id = '{}.{:d}'.format(acc, last_version + 1)
                else:
                    # No record with that accession, that's a new record;
                    # discard the provided accession and force a generated one
                    last_acc += 1
                    record.id = '{}_{:06d}.1'.format(prefix, last_acc)

            # Delete any 'ACCESSION' annotations
            if 'accessions' in record.annotations:
                record.annotations.pop('accessions')

            # Delete empty 'ORGANISMS' annotations
            if record.annotations.get('organism', '') == '. .':
                record.annotations.pop('organism')
            if len(record.annotations.get('source', ' ')) == 0:
                record.annotations.pop('source')

            # Effectively load the record
            db_loader.load_seqrecord(record)

        return num_records
