from sqlalchemy import text

from tools.helper import dbconnect, postdispatch, respondrest


@respondrest
@dbconnect
def _checkconnection(db):
    res = db.execute(text("SELECT 1"))
    num = next(res)
    return {"res": "OK" if num[0] == 1 else "ERROR"}


@postdispatch
def _action(d):
    d.registergetwhat("checkconnection", _checkconnection)


if __name__ == "__main__":
    _action()
