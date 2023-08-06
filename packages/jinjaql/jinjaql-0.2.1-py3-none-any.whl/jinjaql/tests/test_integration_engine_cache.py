# coding: utf-8
import os
import shutil
import sqlite3
import pathlib
from jinjaql.cache import test as test_cache
from jinjaql.factory import JinJAQL
from jinjaql.engine import sqlite_test

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.sql_root = os.path.abspath(os.path.dirname(__file__))
        self.jinjaql_engine = JinJAQL(pathlib.Path(self.sql_root, 'queries'), engine=sqlite_test)
        self.jinjaql_engine_cache = JinJAQL(pathlib.Path(self.sql_root, 'queries'), engine=sqlite_test, cache=test_cache)
        self.sqlite_folder = os.path.join(self.sql_root, 'data')
        self.sqlite_path = os.path.join(self.sqlite_folder, 'test_db.sqlite')
        if not os.path.exists(self.sqlite_folder):
            os.makedirs(self.sqlite_folder)
        if not os.path.exists(self.sqlite_path):
            open(self.sqlite_path, 'a').close()

    def tearDown(self):
        shutil.rmtree(self.sqlite_folder)

    def test_engine(self):
        queries = self.jinjaql_engine.load_queries('integration.sql')
        try:
            queries.create_artists()
        except:
            pass
        query = queries.insert_artist(**{
            'id': 1,
            'name': 'Lana Del Rey',
            'age': 30,
            'instrument': 'voice',
            'creation_date': '2015-10-13',
        })
        result = queries.get_artists(id=1)

        self.assertEqual(result, [('Lana Del Rey', 30, 'voice')])

    def test_engine_cache(self):
        queries = self.jinjaql_engine_cache.load_queries('integration.sql')
        try:
            queries.create_artists()
        except:
            pass
        query = queries.insert_artist(**{
            'id': 1,
            'name': 'Lana Del Rey',
            'age': 30,
            'instrument': 'voice',
            'creation_date': '2015-10-13',
        })
        result = queries.get_artists(id=1)

        self.assertEqual(result, [('Lana Del Rey', 30, 'voice'), ('Lana Del Rey', 32, 'voice')])