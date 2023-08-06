# pylint: skip-file
import asyncio
import unittest

from sqlalchemy import select
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from .. import query


Base = declarative_base()


class NamedQueryIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        self.engine = create_async_engine('sqlite://')
        self.session_factory = AsyncSession(self.engine)
        self.session = self.run_sync(self.session_factory.__aenter__)
        self.run_sync(self.create_metadata)

    def tearDown(self):
        self.run_sync(self.session.__aexit__, None, None, None)
        self.run_sync(self.engine.dispose)

    async def create_metadata(self):
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        self.session.add(FooModel(value='foo'))
        self.session.add(FooModel(value='bar'))
        self.session.add(FooModel(value='baz'))
        await self.session.commit()

    def run_sync(self, f, *args, **kwargs):
        return self.loop.run_until_complete(f(*args, **kwargs))

    def test_execute_query_declarative_one(self):
        q = GetFooByValue(value='bar')
        result = self.run_sync(q.run, self.session)
        self.assertEqual(result.value, 'bar')

    def test_execute_query_declarative_list(self):
        q = ListFoo()
        result = self.run_sync(q.run, self.session)
        objects = list(result)
        self.assertEqual(objects[0].value, 'foo')
        self.assertEqual(objects[1].value, 'bar')
        self.assertEqual(objects[2].value, 'baz')


class FooModel(Base):
    __tablename__ = 'bar'
    value = Column(String, primary_key=True)


class GetFooByValue(query.DeclarativeQuery):
    value = query.String()

    def build(self):
        return select(FooModel).where(FooModel.value==self.value)


class ListFoo(query.DeclarativeCollectionQuery):

    def build(self):
        return select(FooModel)
