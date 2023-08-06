"""Declares :mod:`pytest` fixtures to assist in testing."""
import os

import ioc.loader
import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.orm import sessionmaker
from unimatrix.conf import settings

from .. import conf
from .. import create_engine
from .. import destroy_engines


def requires_rdbms(test, *args, **kwargs):
    """Class or function decorator that ensures that the testing database
    is configured during a test session.
    """
    return pytest.mark.usefixtures('setup_databases')(test)


def _setup_sqlite(name, connection):
    connection['name'] = ":memory:"


def _setup_postgres(name, connection):
    db_name = connection['name']
    test_db_name = f"test_{db_name}"

    # Connect to the postgres database (which is assumed to exist) so we
    # can issue the CREATE DATABASE statement.
    engine = create_engine(name)
    session = sessionmaker(bind=engine)()
    session.connection().connection.set_isolation_level(0)
    session.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
    session.execute(f"CREATE DATABASE {test_db_name}")
    connection['name'] = test_db_name


_setup_functions = {
    'postgresql': _setup_postgres,
    'sqlite': _setup_sqlite
}


@pytest.fixture(scope='session')
def setup_databases():
    """Lookup all database connections and reconfigure the internal state
    of the :mod:`unimatrix.ext.orm` package. Run the migrations using
    alembic.
    """
    test_databases = {}
    for name in dict.keys(conf.DATABASES):
        connection = conf.DATABASES[name]
        _setup_functions[ connection['engine'] ](name, connection)

    # Ensure that all engines are disposed and sessions closed. All new
    # engines and sessions connect to the test database.
    if not os.path.exists('alembic.ini'):
        return
    self = conf.DATABASES['self']
    target_metadata = ioc.loader.import_symbol(settings.SQL_METADATA)
    dsn = self.as_dsn()
    config = Config('alembic.ini')
    config.set_main_option("sqlalchemy.url", dsn)
    script = ScriptDirectory.from_config(config)
    context = EnvironmentContext(config, script)
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    def do_upgrade(revision, context):
        return script._upgrade_revs(script.get_heads(), revision)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            fn=do_upgrade
        )

        with context.begin_transaction():
            context.run_migrations()

    destroy_engines()
