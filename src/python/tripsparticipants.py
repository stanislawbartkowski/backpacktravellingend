
from sqlalchemy import delete, insert, select
from tools.helper import Notitication, dbtable, gennotification, genvars, postdispatch, respondrest

# pk_trips

_TABLE = 'trip_participant'
_PARTICIPANTS = 'participants'


def _dajpk(w):
    return w.get('pk_trips')


@dbtable(_TABLE)
@respondrest
def _updateparticipants(conn, table, w):
    pk = _dajpk(w)
    stmt = delete(table).where(table.c.trip_id == pk)
    conn.execute(stmt)
    participants = w.get(_PARTICIPANTS)
    pars = {
        'trip_id': pk
    }
    for id in participants:
        pars['user_id'] = id
        print(pars)
        stmt = insert(table).values([pars])
        print(stmt)
        conn.execute(stmt)
    conn.commit()
    searchR = {"pk_trips": pk}
    pars = {
        "refresh": True,
        "close": True,
        "searchR": searchR
    }
    res = gennotification(Notitication.SUCCESS, None,
                          "List of participants was updated", **pars)
    return res


@dbtable(_TABLE)
@respondrest
def _initparticipants(conn, table, w):
    pk = _dajpk(w)
    participants: list[int] = []
    query = select(table).where(table.c.trip_id == pk)
    res = conn.execute(query)
    for row in res:
        user_id = row.user_id
        participants.append(user_id)
    return {
        _PARTICIPANTS: participants
    }


@postdispatch
def _actions(d):
    d.registerwhat('initparticipants', _initparticipants)
    d.registerwhat('updateparticipants', _updateparticipants)
    pass


if __name__ == "__main__":
    _actions()
