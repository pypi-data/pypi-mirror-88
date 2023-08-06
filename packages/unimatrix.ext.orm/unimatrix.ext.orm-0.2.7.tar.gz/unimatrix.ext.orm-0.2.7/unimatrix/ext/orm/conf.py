"""Provides functions to configure the database connection(s)."""
import copy
import os

import unimatrix.lib.rdbms
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


class DatabaseConnection(dict):
    """Represents a database connection configuration."""

    @property
    def name(self):
        return self['connection']

    def wait(self, timeout=3):
        """Block until the connection is available."""
        engine = self.as_engine(create_engine)
        try:
            engine.connect()
        except OperationalError:
            return None
        finally:
            engine.dispose()
        return self

    def as_dsn(self, use_async=False):
        """Returns the connection credentials as a data source name."""
        if self['engine'] == 'sqlite' and self.get('name') == ':memory:':
            return "sqlite://"
        elif self['engine'] == 'sqlite':
            return f"sqlite:///{self['name']}"
        elif self['engine'] == 'postgresql':
            scheme = 'postgresql+psycopg2'
            if use_async:
                scheme = 'postgresql+asyncpg'
            dsn = f"{scheme}://"
            if self.get('username'):
                dsn += self['username']
                if self.get('password'):
                    dsn += f":{self['password']}"
                dsn += "@"
            dsn += f"{self.get('host') or 'localhost'}"
            dsn += f":{self.get('port') or 5432}"
            if self.get('name'):
                dsn += f"/{self['name']}"
            return dsn
        else:
            raise NotImplementedError # pragma: no cover

    def as_engine(self, create_engine, *args, **kwargs):
        """Return a :class:`sqlalchemy.engine.Engine` instance configured
        with the connection parameters.
        """
        return create_engine(self.as_dsn(kwargs.pop('use_async', False)),
            *args, **kwargs)


def load_config(*args, **kwargs):
    """Like :func:`~unimatrix.lib.rdbms.load_config`, but returns a mapping
    of :class:`DatabaseConnection` objects.
    """
    connections = unimatrix.lib.rdbms.load_config(*args, **kwargs)
    for name, opts in dict.items(connections):
        connections[name] = DatabaseConnection({'connection': name, **opts})
    return connections


DATABASES = load_config(env=copy.deepcopy(os.environ))
