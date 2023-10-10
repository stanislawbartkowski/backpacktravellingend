from testmixin import MixinTest


class TestTransportation(MixinTest):

    def _addtransportation(self):
        trip: dict = self._add_trip()
        trip_id: int = trip['pk_trips']

        data: dict = {
            'pk_trips': trip_id,
            'airline': "Hello"
        }
        r = self._transportationaction("add", data)
        print(r)
        tr: list[dict] = self._gettransportation(trip_id)
        print(tr)
        assert (1 == len(tr))
        tra: dict = tr[0]
        assert ('Hello' == tra['airline'])
        return tra

    def test_addtransportation(self, del_trips):
        self._addtransportation()

    def test_updatetransportation(self, del_trips):
        tra: dict = self._addtransportation()
        tra['price'] = 1234
        r = self._transportationaction("update", tra)
        print(r)

        trip_id = tra['trip_id']

        tr: list[dict] = self._gettransportation(trip_id)
        assert (1 == len(tr))
        tra: dict = tr[0]
        print(tra)
        assert ('Hello' == tra['airline'])
        assert (1234 == tra['price'])

    def test_deltransportation(self, del_trips):
        tra: dict = self._addtransportation()
        tr_id = tra['pk_ground_transportation']
        trip_id = tra['trip_id']
        r = self._transportationactiondel(tr_id)
        print(r)
        tr: list[dict] = self._gettransportation(trip_id)
        assert (0 == len(tr))
