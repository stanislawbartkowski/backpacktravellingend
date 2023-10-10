from tools.crudop import CRUOP
from tools.helper import FIELD, FTYPE, postdispatch


class TRANSPORTATION(CRUOP):

    _MAPFKEY: tuple[str, str] = ('trip_id', 'pk_trips')
    _TABLE = 'ground_transportation'
    _COLS = ['trip_id', 'airline', 'fromid', 'toid',
             FIELD("transportation_date", FTYPE.DATERANGE,
                   ['departure_time', 'arrival_time']),
             'has_air_con',
             'has_wifi', 'price', 'published_at', 'owner_id', 'latitude', 'longitude']
    _DELNOTIFICATION: str = "Transportation removed from trip"
    _UPDATENOTIFICATION: str = "Transportation data updated"
    _ADDNOTIFICAITON: str = "New transportation added to trip"


@postdispatch(cols=TRANSPORTATION._COLS)
def _actions(d):
    U = TRANSPORTATION()
    U.registerwhat(d)


if __name__ == "__main__":
    _actions()
