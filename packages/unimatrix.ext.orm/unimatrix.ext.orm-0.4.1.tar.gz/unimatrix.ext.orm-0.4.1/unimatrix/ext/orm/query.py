"""Declares :class:`NamedQuery`."""
import marshmallow.exceptions
from marshmallow.fields import *
from marshmallow import Schema
from sqlalchemy.orm.exc import NoResultFound
from unimatrix.ext.model.exc import ValidationError


FORBIDDEN_ATTRS = ['build', 'execute', 'schema_context']


class NamedQueryParameter:

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls=None):
        return obj._params[self.name]


class NamedQueryMeta(type):

    def __new__(cls, name, bases, attrs):
        super_new = super().__new__
        if name == 'NamedQuery':
            return super_new(cls, name, bases, attrs)

        # Construct a marshmallow.Schema class based on the fields found
        # on the NamedQuery subclass.
        fields = {}
        for attname in list(dict.keys(attrs)):
            if not isinstance(attrs[attname], Field):
                continue
            if attname in FORBIDDEN_ATTRS:
                raise ValueError("Field name '%s' is not allowed" % attname)
            fields[attname] = attrs.pop(attname)
            attrs[attname] = NamedQueryParameter(attname)

        attrs['schema_class'] = type("%sSchema" % name, (Schema,), fields)

        return super_new(cls, name, bases, attrs)


class NamedQuery(metaclass=NamedQueryMeta):
    """Represents a named database query."""
    declarative = False

    def __init__(self, *args, **kwargs):
        schema = self.schema_class()
        try:
            self._params = schema.load(kwargs)
        except marshmallow.exceptions.ValidationError as e:
            raise ValidationError(spec=e.normalized_messages())
        self._query = None

    def build(self):
        """Builds the query."""
        raise NotImplementedError

    def process_result(self, result):
        """Hook to process the query results."""
        return result

    def _build(self):
        self._query = self.build()
        return self._query

    def _process_result(self, result):
        return self.process_result(result)

    async def run(self, session):
        """Run the query."""
        return Result(self, await self.execute(session))

    async def execute(self, session):
        """Executes the query and returns the result."""
        return self._process_result(await session.execute(self._build()))


class BaseDeclarativeQuery(NamedQuery):
    """A :class:`~unimatrix.ext.orm.query.Query` implementation that
    process the result as an SQLAlchemy declarative model.
    """

    def process_result(self, result):
        return result.scalars()


class DeclarativeCollectionQuery(BaseDeclarativeQuery):
    """Like :class:`BaseDeclarativeQuery`, but expects a collection."""

    def process_result(self, result):
        return result.scalars()


class DeclarativeQuery(BaseDeclarativeQuery):
    """Like :class:`BaseDeclarativeQuery`, but expects a single entity
    to be returned.
    """

    #: Indicates if the result may be ``None``.
    allow_none = False

    def process_result(self, result):
        result = super().process_result(result)
        return result.one() if not self.allow_none else result.first()


class Get(NamedQuery):
    """A :class:`Query` implementation that results a single row."""
    allow_none = False

    def process_result(self, result):
        result = result.fetchone()
        if result is None and not self.allow_none:
            raise NoResultFound
        return result


class Result:
    """The result of an executed :class:`Query`."""
    not_provided = object()

    def __init__(self, query, result):
        self.__query = query
        self.__result = result

    def __getattr__(self, attname):
        return getattr(self.__result, attname)

    def __iter__(self):
        return iter(self.__result)


Query = NamedQuery
