from testmixin import MixinTest


class TestFlight(MixinTest):

    def _addflight(self):
        trip: dict = self._add_trip()
        trip_id: int = trip['pk_trips']

        data: dict = {
            'pk_trips': trip_id,
            'airline': "Hello"
        }
        r = self._flightaction("add", data)
        print(r)
        fl: list[dict] = self._getflight(trip_id)
        print(fl)
        assert (1 == len(fl))
        fli: dict = fl[0]
        assert ('Hello' == fli['airline'])
        return fli

    def test_addflight(self, del_trips):
        fli = self._addflight()
        print(fli)

    def test_updateflight(self, del_trips):
        fli: dict = self._addflight()
        fli['price'] = 1234
        r = self._flightaction("update", fli)
        print(r)

        trip_id = fli['trip_id']

        fl: list[dict] = self._getflight(trip_id)
        assert (1 == len(fl))
        fli: dict = fl[0]
        print(fli)
        assert ('Hello' == fli['airline'])
        assert (1234 == fli['price'])

    def test_delflight(self, del_trips):
        fli: dict = self._addflight()
        fli_id = fli['pk_flights']
        trip_id = fli['trip_id']
        r = self._flightactiondel(fli_id)
        print(r)
        tr: list[dict] = self._getflight(trip_id)
        assert (0 == len(tr))
