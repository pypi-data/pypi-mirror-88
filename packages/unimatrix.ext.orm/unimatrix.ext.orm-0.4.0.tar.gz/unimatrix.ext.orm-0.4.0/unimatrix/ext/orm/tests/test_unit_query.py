# pylint: skip-file
import asyncio

import unittest
import unittest.mock

from unimatrix.lib.datastructures import ImmutableDTO
from unimatrix.ext.model.exc import ValidationError

from .. import query


class NamedQueryTestCase(unittest.TestCase):

    class query_class(query.NamedQuery):
        foo = query.String(required=True)

        def build(self):
            return None

    def test_instantiate_with_valid_parameters(self):
        q = self.query_class(foo='bar')

    def test_instantiate_with_invalid_parameters(self):
        with self.assertRaises(ValidationError):
            q = self.query_class(foo=1)

    def test_parameter_descriptor(self):
        q = self.query_class(foo='bar')
        self.assertEqual(q.foo, 'bar')

    def test_cannot_create_class_with_forbidden_attribute(self):
        with self.assertRaises(ValueError):
            type('Foo', (query.NamedQuery,), {
                'build': query.String()
            })

    def test_run_does_emit_query(self):
        exc = Exception()
        q = self.query_class(foo='bar')
        f = q.run(ImmutableDTO(execute=unittest.mock.AsyncMock(side_effect=exc)))
        try:
            result = asyncio.run(f)
        except Exception  as e:
            self.assertEqual(e, exc)
