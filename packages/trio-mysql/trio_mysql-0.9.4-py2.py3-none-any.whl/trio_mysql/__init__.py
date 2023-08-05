"""
Trio-MySQL: A pure-Python MySQL client library.

Copyright (c) 2010-2016 PyMySQL contributors
Copyright (c) 2018 Trio-MySQL contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import sys

from ._version import VERSION
from .constants import FIELD_TYPE
from .converters import escape_dict, escape_sequence, escape_string
from .err import (
    Warning, Error, InterfaceError, DataError,
    DatabaseError, OperationalError, IntegrityError, InternalError,
    NotSupportedError, ProgrammingError, MySQLError)
from .times import (
    Date, Time, Timestamp,
    DateFromTicks, TimeFromTicks, TimestampFromTicks)


if VERSION[3] is not None:
    VERSION_STRING = "%d.%d.%d_%s" % VERSION
else:
    VERSION_STRING = "%d.%d.%d" % VERSION[:3]
threadsafety = 1
apilevel = "2.0"
paramstyle = "pyformat"


class DBAPISet(frozenset):

    def __ne__(self, other):
        if isinstance(other, set):
            return frozenset.__ne__(self, other)
        else:
            return other not in self

    def __eq__(self, other):
        if isinstance(other, frozenset):
            return frozenset.__eq__(self, other)
        else:
            return other in self

    def __hash__(self):
        return frozenset.__hash__(self)


STRING    = DBAPISet([FIELD_TYPE.ENUM, FIELD_TYPE.STRING,
                     FIELD_TYPE.VAR_STRING])
BINARY    = DBAPISet([FIELD_TYPE.BLOB, FIELD_TYPE.LONG_BLOB,
                     FIELD_TYPE.MEDIUM_BLOB, FIELD_TYPE.TINY_BLOB])
NUMBER    = DBAPISet([FIELD_TYPE.DECIMAL, FIELD_TYPE.DOUBLE, FIELD_TYPE.FLOAT,
                     FIELD_TYPE.INT24, FIELD_TYPE.LONG, FIELD_TYPE.LONGLONG,
                     FIELD_TYPE.TINY, FIELD_TYPE.YEAR])
DATE      = DBAPISet([FIELD_TYPE.DATE, FIELD_TYPE.NEWDATE])
TIME      = DBAPISet([FIELD_TYPE.TIME])
TIMESTAMP = DBAPISet([FIELD_TYPE.TIMESTAMP, FIELD_TYPE.DATETIME])
DATETIME  = TIMESTAMP
ROWID     = DBAPISet()


def Binary(x):
    """Return x as a binary type."""
    return bytes(x)


def Connect(*args, **kwargs):
    """
    Connect to the database; see connections.Connection.__init__() for
    more information.

    Note that you need to use ``async with`` in order to actually use the connection!
    """
    from .connections import Connection
    return Connection(*args, **kwargs)

from . import connections as _orig_conn
if _orig_conn.Connection.__init__.__doc__ is not None:
    Connect.__doc__ = _orig_conn.Connection.__init__.__doc__
del _orig_conn


def get_client_info():  # for MySQLdb compatibility
    version = VERSION
    if VERSION[3] is None:
        version = VERSION[:3]
    return '.'.join(map(str, version))

connect = Connection = Connect

version_info = (0, 1, 0, "alpha", 0)

NULL = "NULL"

__version__ = get_client_info()

def thread_safe():
    return True  # match MySQLdb.thread_safe()

__all__ = [
    'BINARY', 'Binary', 'Connect', 'Connection', 'DATE', 'Date',
    'Time', 'Timestamp', 'DateFromTicks', 'TimeFromTicks', 'TimestampFromTicks',
    'DataError', 'DatabaseError', 'Error', 'FIELD_TYPE', 'IntegrityError',
    'InterfaceError', 'InternalError', 'MySQLError', 'NULL', 'NUMBER',
    'NotSupportedError', 'DBAPISet', 'OperationalError', 'ProgrammingError',
    'ROWID', 'STRING', 'TIME', 'TIMESTAMP', 'Warning', 'apilevel', 'connect',
    'connections', 'constants', 'converters', 'cursors',
    'escape_dict', 'escape_sequence', 'escape_string', 'get_client_info',
    'paramstyle', 'threadsafety', 'version_info',

    "NULL", "__version__",
]
