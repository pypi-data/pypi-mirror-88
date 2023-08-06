import random
import typing
from datetime import datetime
from functools import lru_cache

from sqlalchemy import Column, Table, MetaData, create_engine

from bakplane.bakplane_pb2 import ResolveResourcePathResponse, ResolveResourceIntentResponse
from bakplane.extensions.base import WriteRequest, ConnectionStringContext, ReadResponse, ReadAllRequest, ReadRequest
from bakplane.extensions.spark import PluginEntry, WriteResponse
from bakplane.extensions.spark.stores.jdbc import DataStoreHelper

DRIVER_NAME = 'com.amazon.redshift.jdbc42.Driver'


class RedshiftStoreHelper(DataStoreHelper):
    def __init__(self, user: str, password: str, host: str, port: int, database: str, schema_name: str):
        self.metadata = MetaData()
        self.engine = create_engine(f'redshift+psycopg2://{user}:{password}@{host}:{port}/{database}')
        self.schema_name = schema_name

    def create_temporary_table(self, prefix: str, columns: typing.List[Column],
                               rows: typing.List[typing.Dict[str, typing.Any]]) -> Table:
        tbl = Table(
            prefix + '_' + str(int(datetime.utcnow().timestamp())) + '_' + str(random.randint(1, 1000)),
            self.metadata,
            *columns,
            schema=self.schema_name
        )

        self.metadata.create_all(self.engine)
        self.engine.execute(tbl.insert(), rows)

        return tbl


def get_registration():
    return PluginEntry(
        name='Redshift',
        code='redshift',
        description='Redshift store',
        author='Isaac Elbaz',
        read_fn=__read_fn,
        read_all_fn=__read_all_fn,
        write_fn=__write_fn,
        connection_string_url_fn=__connection_string_url,
        driver_name=DRIVER_NAME
    )


@lru_cache
def get_helper(user: str, password: str, host: str, port: int, database: str, schema_name: str):
    return RedshiftStoreHelper(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
        schema_name=schema_name
    )


def __connection_string_url(c: ConnectionStringContext) -> str:
    return f'jdbc:redshift://{c.context["host"]}:{c.context["port"]}/{c.context["database"]}'


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
        driver=DRIVER_NAME,
        store_helper=get_helper(
            user=res.context['username'],
            password=res.context['password'],
            host=res.context['host'],
            port=res.context['port'],
            database=res.context['database'],
            schema_name='temp_data'
        )
    )
