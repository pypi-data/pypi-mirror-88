##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

import os
import uuid
from typing import List

import cbor2
import click
import numpy as np

import zlmdb
import cfxdb
from cfxdb.xbrnetwork import Account, UserKey

from txaio import time_ns


class Exporter(object):
    """
    CFXDB database exporter.
    """
    def __init__(self, dbpath):
        """

        :param dbpath: Database file to open.
        """
        self._dbpath = os.path.abspath(dbpath)
        self._db = zlmdb.Database(dbpath=self._dbpath, maxsize=2**30, readonly=False)
        self._db.__enter__()

        self._meta = cfxdb.meta.Schema.attach(self._db)
        self._globalschema = cfxdb.globalschema.GlobalSchema.attach(self._db)
        self._mrealmschema = cfxdb.mrealmschema.MrealmSchema.attach(self._db)
        self._xbr = cfxdb.xbr.Schema.attach(self._db)
        self._xbrmm = cfxdb.xbrmm.Schema.attach(self._db)
        self._xbrnetwork = cfxdb.xbrnetwork.Schema.attach(self._db)

        self._schemata = {
            'meta': self._meta,
            'globalschema': self._globalschema,
            'mrealmschema': self._mrealmschema,
            'xbr': self._xbr,
            'xbrmm': self._xbrmm,
            'xbrnetwork': self._xbrnetwork,
        }

        self._schema_tables = {}

        for schema_name, schema in self._schemata.items():
            tables = {}
            first = None
            for k, v in schema.__annotations__.items():
                for line in v.__doc__.splitlines():
                    line = line.strip()
                    if line != "":
                        first = line[:80]
                        break
                tables[k] = first
            self._schema_tables[schema_name] = tables

    @property
    def dbpath(self) -> str:
        """

        :return:
        """
        return self._dbpath

    def schemata(self) -> List[str]:
        """

        :return:
        """
        return sorted(self._schemata.keys())

    def tables(self, schema_name):
        """

        :param schema_name:
        :return:
        """
        if schema_name in self._schema_tables:
            return sorted(self._schema_tables[schema_name].keys())
        else:
            return None

    def table_docs(self, schema_name, table_name):
        """

        :param schema_name:
        :param table_name:
        :return:
        """
        if schema_name in self._schema_tables and table_name in self._schema_tables[schema_name]:
            return self._schema_tables[schema_name][table_name]
        else:
            return None

    def _add_test_data(self):
        account = Account()
        account.oid = uuid.uuid4()
        account.created = np.datetime64(time_ns(), 'ns')
        account.username = 'alice'
        account.email = 'alice@example.com'
        account.wallet_type = 2  # metamask
        account.wallet_address = os.urandom(20)
        # account.wallet_address = binascii.a2b_hex('f5173a6111B2A6B3C20fceD53B2A8405EC142bF6')

        userkey = UserKey()
        userkey.pubkey = os.urandom(32)
        # userkey.pubkey = binascii.a2b_hex('b7e6462121b9632b2bfcc5a3beef0b49dd865093ad003d011d4abbb68476d5b4')
        userkey.created = account.created
        userkey.owner = account.oid

        with self._db.begin(write=True) as txn:
            self._xbrnetwork.accounts[txn, account.oid] = account
            self._xbrnetwork.user_keys[txn, userkey.pubkey] = userkey

    def print_slots(self, include_description=False):
        """

        :param include_description:
        :return:
        """
        print('\nDatabase slots [dbpath="{dbpath}"]:\n'.format(dbpath=self._dbpath))
        slots = self._db._get_slots()
        for slot_id in slots:
            slot = slots[slot_id]
            if include_description:
                print('   Slot {} using DB table class {}: {}'.format(
                    click.style(str(slot_id), fg='white', bold=True), click.style(slot.name, fg='yellow'),
                    slot.description))
            else:
                print('   Slot {} using DB table class {}'.format(
                    click.style(str(slot_id), fg='white', bold=True), click.style(slot.name, fg='yellow')))
        print('')

    def print_stats(self):
        """

        :return:
        """
        print('\nDatabase table statistics [dbpath="{dbpath}"]:\n'.format(dbpath=self._dbpath))
        stats = {}
        with self._db.begin() as txn:
            for schema_name in self._schemata:
                stats[schema_name] = {}
                for table_name in self._schema_tables[schema_name]:
                    table = self._schemata[schema_name].__dict__[table_name]
                    cnt = table.count(txn)
                    stats[schema_name][table_name] = cnt
        for schema_name in stats:
            for table_name in stats[schema_name]:
                cnt = stats[schema_name][table_name]
                if cnt:
                    print('{:.<52}: {}'.format(
                        click.style('{}.{}'.format(schema_name, table_name), fg='white', bold=True),
                        click.style(str(cnt) + ' records', fg='yellow')))

    def export_database(self, filename, include_indexes=False, include_schemata=None, exclude_tables=None):
        """

        :param filename:
        :param include_indexes:
        :return:
        """
        if include_schemata is None:
            schemata = sorted(self._schemata.keys())
        else:
            assert type(include_schemata) == list
            schemata = sorted(list(set(include_schemata).intersection(self._schemata.keys())))

        if exclude_tables is None:
            exclude_tables = set()
        else:
            assert type(exclude_tables) == list
            exclude_tables = set(exclude_tables)

        result = {}
        with self._db.begin() as txn:
            for schema_name in schemata:
                for table_name in self._schema_tables[schema_name]:
                    fq_table_name = '{}.{}'.format(schema_name, table_name)
                    if fq_table_name not in exclude_tables:
                        table = self._schemata[schema_name].__dict__[table_name]
                        if not table.is_index() or include_indexes:
                            recs = []
                            for key, val in table.select(txn, return_keys=True, return_values=True):
                                if val:
                                    if hasattr(val, 'marshal'):
                                        val = val.marshal()
                                recs.append((table._serialize_key(key), val))
                            if recs:
                                if schema_name not in result:
                                    result[schema_name] = {}
                                result[schema_name][table_name] = recs

        data = cbor2.dumps(result)
        with open(filename, 'wb') as f:
            f.write(data)

        # data_recovered = cbor2.loads(data)
        print('\nExported database [dbpath="{dbpath}", filename="{filename}", filesize={filesize}]:\n'.format(
            dbpath=self._dbpath, filename=filename, filesize=len(data)))

        for schema_name in result:
            for table_name in result[schema_name]:
                cnt = len(result[schema_name][table_name])
                if cnt:
                    print('{:.<52}: {}'.format(
                        click.style('{}.{}'.format(schema_name, table_name), fg='white', bold=True),
                        click.style(str(cnt) + ' records', fg='yellow')))

    def import_database(self, filename, include_indexes=False, include_schemata=None, exclude_tables=None):
        """

        :param filename:
        :param include_indexes:
        :return:
        """
        if include_schemata is None:
            schemata = sorted(self._schemata.keys())
        else:
            assert type(include_schemata) == list
            schemata = sorted(list(set(include_schemata).intersection(self._schemata.keys())))

        if exclude_tables is None:
            exclude_tables = set()
        else:
            assert type(exclude_tables) == list
            exclude_tables = set(exclude_tables)

        with open(filename, 'rb') as f:
            data = f.read()
            db_data = cbor2.loads(data)

        print(
            '\nImporting database [dbpath="{dbpath}", filename="{filename}", filesize={filesize}]:\n'.format(
                dbpath=self._dbpath, filename=filename, filesize=len(data)))

        with self._db.begin(write=True) as txn:
            for schema_name in schemata:
                for table_name in self._schema_tables[schema_name]:
                    fq_table_name = '{}.{}'.format(schema_name, table_name)
                    if fq_table_name not in exclude_tables:
                        table = self._schemata[schema_name].__dict__[table_name]
                        if not table.is_index() or include_indexes:
                            if schema_name in db_data and table_name in db_data[schema_name]:
                                cnt = 0
                                for key, val in db_data[schema_name][table_name]:
                                    key = table._deserialize_key(key)
                                    val = table.parse(val)
                                    table[txn, key] = val
                                    cnt += 1
                                if cnt:
                                    print('{:.<52}: {}'.format(
                                        click.style('{}.{}'.format(schema_name, table_name),
                                                    fg='white',
                                                    bold=True), click.style(str(cnt) + ' records',
                                                                            fg='yellow')))
                            else:
                                print('No data to import for {}.{}!'.format(schema_name, table_name))
