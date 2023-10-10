from testmixin import MixinTest


class TestEvents(MixinTest):

    def test_eve(self, del_trips):
        trip: dict = self._add_trip()
        trip_id: int = trip['pk_trips']

        # add flight
        data: dict = {
            'pk_trips': trip_id,
            'airline': "Hello"
        }
        r = self._flightaction("add", data)
        print(r)

        # add transportation
        data: dict = {
            'pk_trips': trip_id,
            'airline': "Hello"
        }
        r = self._transportationaction("add", data)
        print(r)

        # add stays
        data: dict = {
            'pk_trips': trip_id,
            'room_id': 11,
            'price': 22
        }
        r = self._staysaction("add", data)

        li = self._getevents(trip_id)
        print(li)
        assert (3 == len(li))
