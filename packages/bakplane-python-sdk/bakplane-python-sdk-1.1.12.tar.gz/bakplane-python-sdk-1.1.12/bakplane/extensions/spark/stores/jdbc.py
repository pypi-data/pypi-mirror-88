import typing
import urllib.parse
from datetime import datetime
from timeit import default_timer as timer

from bakplane.bakplane_pb2 import ResolveResourcePathResponse, ResolveResourceIntentResponse, ComparisonType
from bakplane.extensions.base import WriteResponse, WriteRequest, ReadResponse, ReadAllRequest, ReadRequest, \
    ReadRequestBuildingBlocks, DataStoreHelper
from bakplane.extensions.spark.utils import to_spark_save_mode, timestamp_to_date_string, datetime_to_date_string, \
    timestamp_to_datetime
from bakplane.utils import to_execution_statistics


def __build_read_all_query(r: ReadAllRequest, res: ResolveResourcePathResponse) -> str:
    return f'select {", ".join(r.columns)} from {res.context["schema_name"]}.{res.context["table_name"]}'


def __build_read_query(r: ReadRequest, res: ResolveResourceIntentResponse, dialect,
                       store_helper: DataStoreHelper) -> str:
    from sqlalchemy import (
        Table,
        MetaData,
        Column,
        select,
        and_,
    )
    metadata: MetaData = MetaData()

    src_tbl: Table = Table(
        res.table_name,
        metadata,
        *[Column(x.name) for x in res.columns],
        schema=res.schema_name,
    )

    mapping_tbl: Table = Table(
        res.mapping.table_name,
        metadata,
        *[Column(x.name) for x in res.mapping.columns],
        schema=res.mapping.schema_name,
    )

    a = src_tbl.alias('a')

    mapping_columns = []
    for column in res.mapping.columns:
        if not column.is_effective_dating:
            mapping_columns.append(
                mapping_tbl.c.get(column.name).label(column.name)
            )

    m = mapping_tbl.alias('m')
    clauses = []
    for clause in res.mapping.clauses:
        if clause.comparison == ComparisonType.EQ:
            clauses.append(
                m.c.get(clause.mapping_field_name) == a.c.get(clause.resource_field_name)
            )


    effective_start_dt = timestamp_to_date_string(res.effective_dating.end_dt.seconds)
    effective_end_dt = timestamp_to_date_string(res.effective_dating.end_dt.seconds)

    blocks = ReadRequestBuildingBlocks(
        mapping_table=m,
        asset_table=a,
        selectable=m.join(a, and_(*clauses)),
        effective_start_dt=timestamp_to_datetime(res.effective_dating.start_dt.seconds),
        effective_end_dt=timestamp_to_datetime(res.effective_dating.end_dt.seconds),
        knowledge_start_dt=r.knowledge_start_dt,
        knowledge_end_dt=r.knowledge_end_dt,
        constraints=[]
    )

    if r.columns:
        blocks.columns = [a.c.get(x) for x in r.columns if x in a.c]
    else:
        blocks.columns = [a.c.get(x) for x in res.columns]

    if r.query_builder:
        res = r.query_builder(blocks)
    else:

        blocks.constraints = []

        if r.additional_constraints is not None:
            blocks.constraints.append(r.additional_constraints)

        if r.effective_dating_hint is None:
            blocks.constraints.append(a.c.effective_start_dt <= m.c.effective_end_dt)
            blocks.constraints.append(a.c.effective_end_dt >= m.c.effective_start_dt)
            blocks.constraints.append(a.c.effective_start_dt <= timestamp_to_date_string(res.effective_dating.end_dt.seconds))
            blocks.constraints.append(a.c.effective_end_dt >= timestamp_to_date_string(res.effective_dating.start_dt.seconds))
        else:
            if isinstance(r.effective_dating_hint, tuple):
                s = datetime_to_date_string(typing.cast(datetime, r.effective_dating_hint[0]))
                e = datetime_to_date_string(typing.cast(datetime, r.effective_dating_hint[1]))

                blocks.constraints.append(a.c.effective_start_dt <= e)
                blocks.constraints.append(a.c.effective_end_dt >= s)
            elif isinstance(r.effective_dating_hint, str):
                col = typing.cast(str, r.effective_dating_hint)

                s = col + '_start_dt'
                e = col + '_end_dt'

                blocks.constraints.append(a.c.effective_start_dt <= m.c.get(e))
                blocks.constraints.append(a.c.effective_end_dt >= m.c.get(s))
            else:
                raise RuntimeError('Invalid type for effective_dating_hint.')

        if r.modifiers:
            for m in r.modifiers:
                blocks = m.execute(blocks, store_helper)

        res = (
            select(blocks.columns)
                .select_from(blocks.selectable)
                .where(and_(*blocks.constraints))
        )

    query = str(
        res.compile(
            dialect=dialect,
            compile_kwargs={"literal_binds": True},
        )
    )

    return query


def write_fn(r: WriteRequest, res: ResolveResourcePathResponse, driver: str, url: str) -> WriteResponse:
    start = timer()

    r.df.write \
        .format('jdbc') \
        .mode(to_spark_save_mode(r.mode)) \
        .option('driver', driver) \
        .option('url', url) \
        .option('dbtable', f"{res.context['schema_name']}.{res.context['table_name']}") \
        .option('user', res.context['username']) \
        .option('password', urllib.parse.unquote(res.context['password'])) \
        .save()

    end = timer()

    return WriteResponse(
        execution_statistics=to_execution_statistics(start, end)
    )


def __read_query(spark, url: str, driver: str, query: str, user: str, password: str):
    start = timer()

    df = spark.read.format('jdbc') \
        .option('url', url) \
        .option('query', query) \
        .option('user', user) \
        .option('password', urllib.parse.unquote(password)) \
        .option('driver', driver) \
        .load()

    end = timer()

    return ReadResponse(
        df=df,
        execution_statistics=to_execution_statistics(start, end),
        context={
            'query': query,
        }
    )


def read_all_fn(ctx: typing.Any, r: ReadAllRequest, res: ResolveResourcePathResponse, url: str,
                driver: str) -> ReadResponse:
    return __read_query(
        spark=ctx,
        url=url,
        driver=driver,
        query=__build_read_all_query(r, res),
        user=res.context['username'],
        password=res.context['password']
    )


def read_fn(ctx: typing.Any, r: ReadRequest, res: ResolveResourceIntentResponse, dialect, url: str,
            driver: str, store_helper: DataStoreHelper) -> ReadResponse:
    return __read_query(
        spark=ctx,
        url=url,
        driver=driver,
        query=__build_read_query(r, res, dialect, store_helper),
        user=res.context['username'],
        password=res.context['password']
    )
