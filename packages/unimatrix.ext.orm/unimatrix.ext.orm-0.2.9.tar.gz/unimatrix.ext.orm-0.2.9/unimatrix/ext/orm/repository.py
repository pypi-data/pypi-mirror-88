"""Declares :class:`RelationalDatabaseRepository`."""
import ioc


class RelationalDatabaseRepository:
    """A repository implementation for use with :mod:`sqlalchemy`."""
    session_factory = 'AsyncSessionFactory'

    async def __aenter__(self):
        self._manages_session = False
        if getattr(self, 'session', None) is None:
            self._manages_session = True
            if isinstance(self.session_factory, str):
                self.session = ioc.require(self.ioc_session_factory_key)()
            elif callable(self.session_factory):
                self.session = self.session_factory()
            else:
                raise NotImplementedError(
                    'Provide an inversion-of-control key as the session_factory'
                    ' attribute or implement it as a method.'
                )

        # Determine if there is a transaction running. If a transaction is
        # running, start a savepoint, else begin a new one.
        begin = self.session.begin
        if self.session.sync_session.in_transaction():
            begin = self.session.begin_nested
        self.tx = begin()
        await self.tx.__aenter__()
        return self

    async def __aexit__(self, cls, exc, tb):
        try:
            await self.tx.__aexit__(cls, exc, tb)
        finally:
            if self._manages_session:
                await self.session.close()

