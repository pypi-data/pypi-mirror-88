import typing

from bakplane.bakplane_pb2 import ResolveResourcePathResponse, ResolveResourceIntentResponse
from bakplane.extensions.base import WriteRequest, ConnectionStringContext, ReadResponse, ReadAllRequest, ReadRequest
from bakplane.extensions.spark import PluginEntry, WriteResponse

DRIVER_NAME = 'org.postgresql.Driver'


def get_registration():
    return PluginEntry(
        name='Postgres',
        code='postgres',
        description='Postgres compatible store',
        author='Isaac Elbaz',
        read_fn=__read_fn,
        read_all_fn=__read_all_fn,
        write_fn=__write_fn,
        connection_string_url_fn=__connection_string_url,
        driver_name=DRIVER_NAME
    )


def __connection_string_url(c: ConnectionStringContext) -> str:
    return f'jdbc:postgresql://{c.context["host"]}:{c.context["port"]}/{c.context["database"]}'


def __write_fn(r: WriteRequest, res: ResolveResourcePathResponse) -> WriteResponse:
    from bakplane.extensions.spark.stores.jdbc import write_fn

    return write_fn(
        r=r,
        res=res,
        driver=DRIVER_NAME,
        url=__connection_string_url(ConnectionStringContext(res.context))
    )


def __read_all_fn(ctx: typing.Any, r: ReadAllRequest, res: ResolveResourcePathResponse) -> ReadResponse:
    from bakplane.extensions.spark.stores.jdbc import read_all_fn

    return read_all_fn(
        ctx=ctx,
        r=r,
        res=res,
        url=__connection_string_url(ConnectionStringContext(res.context)),
        driver=DRIVER_NAME
    )


def __read_fn(ctx: typing.Any, r: ReadRequest, res: ResolveResourceIntentResponse) -> ReadResponse:
    from bakplane.extensions.spark.stores.jdbc import read_fn
    from sqlalchemy.dialects import postgresql

    return read_fn(
        ctx=ctx,
        r=r,
        res=res,
        dialect=postgresql.dialect(),
        url=__connection_string_url(ConnectionStringContext(res.context)),
        driver=DRIVER_NAME
    )
