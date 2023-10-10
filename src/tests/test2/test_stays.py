from testmixin import MixinTest


class TestStays(MixinTest):

    def _addstay(self):
        trip: dict = self._add_trip()
        trip_id: int = trip['pk_trips']

        data: dict = {
            'pk_trips': trip_id,
            'room_id': 11,
            'price': 22
        }
        r = self._staysaction("add", data)
        print(r)
        st: list[dict] = self._getstays(trip_id)
        print(st)
        assert (1 == len(st))
        sta: dict = st[0]
        assert (11 == sta['room_id'])
        assert (22 == sta['price'])
        return sta

    def test_addstay(self, del_trips):
        sta = self._addstay()
        print(sta)

    def test_updatestay(self, del_trips):
        sta: dict = self._addstay()
        sta['price'] = 999
        r = self._staysaction("update", sta)
        print(r)

        trip_id = sta['trip_id']

        st: list[dict] = self._getstays(trip_id)
        assert (1 == len(st))
        sta: dict = st[0]
        print(sta)
        assert (999 == sta['price'])
        
    def test_delstaysation(self, del_trips):
        sta: dict = self._addstay()
        st_id = sta['pk_stays']
        trip_id = sta['trip_id']
        r = self._staysactiondel(st_id)
        print(r)
        st: list[dict] = self._getstays(trip_id)
        assert (0 == len(st))
        
