from tools.crudop import CRUOP
from tools.helper import FIELD, FTYPE, postdispatch


class FLIGHT(CRUOP):

    _MAPFKEY: tuple[str, str] = ('trip_id', 'pk_trips')
    _TABLE = 'flights'
    _COLS = ['trip_id', 'airline', 'fromid', 'toid',
             FIELD("flight_date", FTYPE.DATERANGE,
                   ['departure_time', 'arrival_time']),
             'has_air_con',
             'has_wifi', 'price', 'published_at', 'owner_id', 'latitude', 'longitude']
    _DELNOTIFICATION: str = "Flight removed from trip"
    _UPDATENOTIFICATION: str = "Flight data updated"
    _ADDNOTIFICAITON: str = "New flight added to trip"


@postdispatch(cols=FLIGHT._COLS)
def _actions(d):
    U = FLIGHT()
    U.registerwhat(d)


if __name__ == "__main__":
    _actions()
