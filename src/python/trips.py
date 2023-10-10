from tools.crudop import CRUOP
from tools.helper import FIELD, FTYPE, postdispatch


class TRIPS(CRUOP):

    _TABLE = 'trips'
    _COLS = ['name', 'location', 
             FIELD("tripdate", FTYPE.DATERANGE, ['start_time', 'end_time']),
             'flights', 'stays', 'transportation', 'activities']
    _DELNOTIFICATION: str = "Trip deleted"
    _UPDATENOTIFICATION: str = "Trip data updated"
    _ADDNOTIFICAITON: str = "New trip added"


@postdispatch(cols=TRIPS._COLS)
def _actions(d):
    U = TRIPS()
    U.registerwhat(d)


if __name__ == "__main__":
    _actions()
