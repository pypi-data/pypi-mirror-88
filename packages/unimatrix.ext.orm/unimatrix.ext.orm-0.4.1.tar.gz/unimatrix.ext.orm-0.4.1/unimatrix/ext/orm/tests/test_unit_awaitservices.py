# pylint: skip-file
import os
import unittest

from .. import awaitservices
from .. import destroy_engines
from ..conf import load_config


class AwaitServicesTestCase(unittest.TestCase):

    def tearDown(self):
        destroy_engines()

    def test_happy_sqlite(self):
        databases = load_config({
            'DB_ENGINE': 'sqlite',
            'DB_NAME': ":memory:",
        })
        awaitservices(max_retries=1, interval=0.1, databases=databases)

    def test_non_resolvable_hostname_postgresql(self):
        databases = load_config({
            'DB_ENGINE': 'postgresql',
            'DB_NAME': "rdbms",
            'DB_USERNAME': "rdbms",
            'DB_PASSWORD': "rdbms",
            'DB_HOST': bytes.hex(os.urandom(16))
        })
        with self.assertRaises(RuntimeError):
            awaitservices(max_retries=1, interval=0.1, databases=databases)
