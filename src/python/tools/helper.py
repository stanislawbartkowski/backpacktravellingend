from dataclasses import dataclass, field
import os
import sys
import functools
from typing import Dict
from enum import Enum

import logging
import json

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import Session


# ------------------
# logger
# ------------------


def getlog(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    stream = logging.StreamHandler(sys.stdout)
    stream.setLevel(logging.DEBUG)
    log.addHandler(stream)
    return log


_logg = getlog(__name__)

# --------------
# different ui
# --------------


def generrorelem(field, message=None, messagedirect=None):
    if messagedirect is None:
        return {'field': field, 'err': {'message': message}}
    return {'field': field, 'err': {'messagedirect': messagedirect}}


# ---------------
# sql
# ---------------


def dbengine():
    url = os.environ["ENV_alchemyconnect"]
    engine = create_engine(url, future=True)
    return engine


# decorator
def dbconnect(func):
    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        db = dbengine().connect()
        res = func(db, *args, **kwargs)
        db.close()
        return res

    return func_wrapper


def dbsession(func):
    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        engine = dbengine()
        db = engine.connect()
        session = Session(engine)
        res = func(session, *args, **kwargs)
        db.close()
        return res

    return func_wrapper


def dbtable(name):

    def decorate(func):

        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            engine = dbengine()
            db = engine.connect()
            metadata = MetaData(bind=None)
            table = Table(
                name,
                metadata,
                autoload=True,
                autoload_with=engine
            )
            res = func(db, table, *args, **kwargs)
            return res

        return func_wrapper

    return decorate

# --------------
# Decorators
# --------------


def respondrest(func):
    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        json: Dict = func(*args, **kwargs)
        writerest(json or {})

    return func_wrapper


def postdispatch(func=None, cols=None):

    if func is not None:

        def func_wrapper():
            d = _DISPATCH.getpost(None)
            func(d)
            d.execute()

        return func_wrapper

    else:

        def decorate(func):

            def func_wrapper():
                d = _DISPATCH.getpost(cols)
                func(d)
                d.execute()

            return func_wrapper

        return decorate

# -------------
# misc procs
# -------------


class Notitication(Enum):
    SUCCESS = "success"


def gennotification(kind: Notitication, title: str, descr: str, **kwargs) -> dict:
    res = {
        "notification": {
            "kind": kind.value,
            "title": title or '',
            "description": {'messagedirect': descr}
        },
    }
    gvars = genvars(**kwargs)
    return res | gvars


def _tmpfile():
    return os.environ["TMPFILE"]


def genvars(vars=None, next=False, close=False, refresh=False, retprops=None, searchR=None, fieldsprops=None):
    res = {"vars": vars or {}}

    if close:
        res["close"] = True
    if next:
        res["next"] = True
    if refresh:
        res["refresh"] = True
    if retprops is not None:
        res["retprops"] = retprops
    if searchR is not None:
        searchF = {"searchF": {"searchF": searchR}}
        res['vars'].update(searchF)
    if fieldsprops is not None:
        res['fieldsprops'] = fieldsprops
    return res


def writerest(s: dict):
    t = _tmpfile()
    with open(t, "w+") as f:
        ss = json.dumps(s)
        _logg.debug(ss)
        f.write(ss)


def getuploadfile():
    return os.environ["UPLOADEDFILE"]


def getpar(p):
    val = os.environ[p]
    return val


def getparint(p):
    val = getpar(p)
    return int(val)


def _getform():
    u = getuploadfile()
    with open(u) as f:
        j = json.load(f)
        _logg.info(j)
        return j

# -------------------
# JSON parameters
# -------------------


@dataclass
class WJON:

    js: dict = field(default_factory=_getform)

    def get(self, f):
        return self.js.get(f)

    def isnone(self, f):
        return self.js.get(f) is None

    def getdrange(self, f, ind):
        if self.isnone(f):
            return None
        return self.get(f)[ind]

# ------------------
# data class
# ------------------


class FTYPE(Enum):
    STRING = 1
    INT = 2
    LOG = 3
    DATE = 4
    DATERANGE = 5


@dataclass
class FIELD:
    id: str
    type: FTYPE = field(default_factory=FTYPE.STRING)
    drange: list = field(default_factory=None)


class WDATA:

    CURRENT = 'currentfield'

    def __init__(self, w, cols):
        self._w = w
        self._fstring = set()
        self._fieldstring = dict()
        self._cols = cols
        for f in cols:
            if isinstance(f, str):
                self._fstring.add(f)
            else:
                fie: FIELD = f
                if fie.type == FTYPE.DATERANGE:
                    self._fieldstring[fie.drange[0]
                                      ] = lambda: self._w.getdrange(fie.id, 0)
                    self._fieldstring[fie.drange[1]
                                      ] = lambda: self._w.getdrange(fie.id, 1)
                else:
                    self._fieldstring[fie.id] = lambda: self._w.get(fie.id)

    def get(self, f):
        if f in self._fieldstring:
            return self._fieldstring[f]()
        return self._w.get(f)

    def isnone(self, f):
        if f in self._fieldstring:
            res = self._fieldstring[f]()
            return res is None
        return self._w.get(f) is None

    @property
    def current(self):
        return self.get(self.CURRENT)

    @property
    def isnonecurrent(self):
        return self.isnone(self.CURRENT)

    def sql_values(self) -> dict:
        fkeys = [f for f in self._fstring]
        ffkeys = [f for f in self._fieldstring]

        pars = {k: self.get(k) for k in fkeys+ffkeys}
        return pars

    def form_disabled(self) -> dict:
        ffkeys = [f.id for f in self._cols if not isinstance(f, str)]
        fkeys = [f for f in self._fstring]
        disablepars = {k: {"disabled": True} for k in ffkeys + fkeys}
        return disablepars


# ---------------
# DISPATCH
# ---------------


@dataclass
class _DISPATCH:
    d = {}
    cols: list
    isw: bool

    @dataclass
    class FUNC:
        func: object
        isw: bool

    def registerwhat(self, what: str, func):
        self.d[what] = self.FUNC(func, self.isw)

    def registergetwhat(self, what: str, func):
        self.d[what] = self.FUNC(func, False)

    def execute(self):
        what = getpar("what")
        F: self.FUNC = self.d.get(what)
        if F is None:
            _logg.fatal(f'Cannot find dispatch for {what}')
            return
        if F.isw:
            w = WJON()
            if self.cols is None:
                F.func(w)
            else:
                wd = WDATA(w, self.cols)
                F.func(wd)
        else:
            F.func()

    @classmethod
    def getget(cls, cols: list):
        return cls(cols, False)

    @classmethod
    def getpost(cls, cols: list):
        return cls(cols, True)
