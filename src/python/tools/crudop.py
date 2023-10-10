from datetime import datetime, timezone


import functools

from sqlalchemy import insert, text, update, delete
from tools.helper import Notitication, dbtable, gennotification, genvars, getlog, getparint, respondrest, generrorelem

_log = getlog(__name__)


class CRUOP:

    def __init__(self, time_updated=True):
        self._time_updated = time_updated

    _TABLE: str = None
    _COLTODUPLICATE: str = None
    _DELNOTIFICATION: str = None
    _UPDATENOTIFICATION: str = None
    _ADDNOTIFICAITON: str = None

    _MAPFKEY: tuple[str, str] = None

    @property
    def table_name(self):
        return self._TABLE

    @staticmethod
    def getprimarykey(table) -> str:
        primary_key = next(k for k in table.primary_key.columns.keys())
        return primary_key

    def _dbtable(func):
        @functools.wraps(func)
        def func_wrapper(self, *args, **kwargs):

            @dbtable(self.table_name)
            def dbfunc(conn, table, self, *args, **kwargs):
                r = func(self, conn, table, *args, **kwargs)
                return r

            return dbfunc(self, *args, **kwargs)
        return func_wrapper

    def _createpars(self, w, insert: bool) -> dict:
        pars = w.sql_values()
        if self._time_updated:
            if insert:
                pars["created_at"] = datetime.now(timezone.utc)
            pars["updated_at"] = datetime.now(timezone.utc)
        if insert and self._MAPFKEY is not None:
            pars[self._MAPFKEY[0]] =  w.get(self._MAPFKEY[1])
        return pars

    @_dbtable
    @respondrest
    def _add(self, conn, table, w) -> dict:
        pars = self._createpars(w, insert=True)
        _log.info(pars)

        primary_key = self.getprimarykey(table)
        stmt = insert(table).values([pars]).returning(table.c[primary_key])
        _log.info(stmt)
        result = conn.execute(stmt)
        res = result.first()
        primary_value = res[0]
        conn.commit()
        _log.info(str(stmt))
        _log.info(f'Primary key inserted: {primary_key}/{primary_value}')
        return self._returnres(primary_key, primary_value, self._ADDNOTIFICAITON)

    @staticmethod
    def _returnres(primary_key: str, primary_value: int, notification: str) -> dict:
        searchR = {primary_key: primary_value}
        pars = {
            "refresh": True,
            "close": True,
            "searchR": searchR
        }
        res = genvars(**pars) if notification is None else gennotification(
            Notitication.SUCCESS, None, notification, **pars)
        return res

    @_dbtable
    @respondrest
    def _update(self, conn, table, w) -> dict:
        _log.info('update')
        pars = self._createpars(w, insert=False)
        primary_key = self.getprimarykey(table)
        primary_value = w.get(primary_key)
        stmt = update(table).where(
            table.c[primary_key] == primary_value).values(pars)
        _log.info(str(stmt))
        conn.execute(stmt)
        conn.commit()
        return self._returnres(primary_key, primary_value, self._UPDATENOTIFICATION)

    @_dbtable
    @respondrest
    def _duplicatedfield(self, conn, table,  w) -> dict:
        if w.isnonecurrent:
            return
        primary_key = self.getprimarykey(table)
        query = f'select * from {self._TABLE} where {self._COLTODUPLICATE} = :value'
        if not w.isnone(primary_key):
            query = query + f' and {primary_key} <> {w.get(primary_key)} '
        res = conn.execute(text(query), {"value": w.current})
        values = res.first()
        return None if values is None else generrorelem(w.CURRENT, message='duplicatedvalue')

    @_dbtable
    @respondrest
    def _delete(self, conn, table) -> dict:
        primary_key = self.getprimarykey(table)
        primary_value = getparint("pk")
        stmt = delete(table).where(table.c[primary_key] == primary_value)
        _log.info(stmt)
        conn.execute(stmt)
        conn.commit()
        pars = {
            "refresh": True,
            "close": True
        }
        return genvars(**pars) if self._DELNOTIFICATION is None else gennotification(Notitication.SUCCESS, None, self._DELNOTIFICATION, **pars)

    @_dbtable
    @respondrest
    def _initdelete(self, conn, table, w) -> dict:
        disablepars = w.form_disabled()
        return genvars(fieldsprops=disablepars)

    def registerwhat(self, d):
        d.registerwhat("add", self._add)
        d.registerwhat("update", self._update)
        d.registerwhat("duplicatedvalue", self._duplicatedfield)
        d.registergetwhat("delete", self._delete)
        d.registerwhat("initdelete", self._initdelete)
