import datetime
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from sqlalchemy.sql.elements import BooleanClauseList

from bakplane.bakplane_pb2 import Universe, ResolveResourceIntentResponse, ResolveResourcePathResponse

from sqlalchemy import Table


class WriteMode(Enum):
    ERROR_IF_EXISTS = 1
    APPEND = 2
    OVERWRITE = 3
    IGNORE = 4


@dataclass
class ExecutionStatistics:
    elapsed_ms: float


@dataclass
class ConnectionStringContext:
    context: typing.Dict[str, str]


@dataclass
class WriteRequest:
    path: str
    warehouse: str
    df: typing.Any
    mode: WriteMode


@dataclass
class ReadAllRequest:
    path: str
    warehouse: str
    columns: typing.List[str]


@dataclass
class ReadRequestBuildingBlocks:
    asset_table: Table
    mapping_table: Table
    selectable: typing.Any
    effective_start_dt: str
    effective_end_dt: str
    knowledge_start_dt: datetime.datetime = None
    knowledge_end_dt: datetime.datetime = None


@dataclass
class ReadRequest:
    path: str
    warehouse: str
    universe: Universe
    effective_start_dt: datetime.datetime
    effective_end_dt: datetime.datetime
    pointers: typing.Dict[str, str]
    columns: typing.List[str] = None
    knowledge_start_dt: datetime.datetime = None
    knowledge_end_dt: datetime.datetime = None
    query_builder: typing.Callable[[ReadRequestBuildingBlocks], typing.Any] = None
    additional_constraints: typing.Callable[[ReadRequestBuildingBlocks], BooleanClauseList] = None
    effective_dating_hint: typing.Union[str, typing.Tuple[datetime.datetime, datetime.datetime]] = None


@dataclass
class ReadUniverseRequest:
    universe: Universe
    effective_start_dt: datetime.datetime
    effective_end_dt: datetime.datetime
    knowledge_start_dt: datetime.datetime = None
    knowledge_end_dt: datetime.datetime = None


@dataclass
class ReadResponse:
    df: typing.Any
    execution_statistics: ExecutionStatistics
    context: typing.Dict[str, str]


@dataclass
class WriteResponse:
    execution_statistics: ExecutionStatistics


@dataclass
class ReadUniverseResponse:
    df: typing.Any
    execution_statistics: ExecutionStatistics


@dataclass
class PluginEntry:
    name: str
    code: str
    description: str
    author: str
    write_fn: typing.Callable[[WriteRequest, ResolveResourcePathResponse], WriteResponse]
    read_fn: typing.Callable[[typing.Any, ReadRequest, ResolveResourceIntentResponse], ReadResponse]
    read_all_fn: typing.Callable[[typing.Any, ReadAllRequest, ResolveResourcePathResponse], ReadResponse]
    connection_string_url_fn: typing.Callable[[ConnectionStringContext], str]
    driver_name: str


class BaseExtension(ABC):
    @abstractmethod
    def read(self, r: ReadRequest) -> ReadResponse:
        pass

    @abstractmethod
    def read_all(self, r: ReadAllRequest) -> ReadResponse:
        pass

    @abstractmethod
    def write(self, r: WriteRequest) -> WriteResponse:
        pass

    @abstractmethod
    def read_universe(self, r: ReadUniverseRequest) -> ReadUniverseResponse:
        pass
