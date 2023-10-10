from tools.crudop import CRUOP
from tools.helper import FIELD, FTYPE, postdispatch


class STAYS(CRUOP):

    _MAPFKEY: tuple[str, str] = ('trip_id', 'pk_trips')
    _TABLE = 'stays'
    _COLS = ['trip_id', 'room_id', 
             FIELD("stays_date", FTYPE.DATERANGE,
                   ['start_date', 'end_date']),
             'price', 'total']
    _DELNOTIFICATION: str = "Stay removed from trip"
    _UPDATENOTIFICATION: str = "Stay data updated"
    _ADDNOTIFICAITON: str = "New stay added to trip"


@postdispatch(cols=STAYS._COLS)
def _actions(d):
    U = STAYS()
    U.registerwhat(d)


if __name__ == "__main__":
    _actions()