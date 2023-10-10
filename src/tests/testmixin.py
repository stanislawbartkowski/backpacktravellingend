import pytest
from tools.requestmixin import RequestMixin


_URL = "http://localhost:7999"

RequestMixin.url = _URL

TESTNAME = "TEST TRIP TO REMOVE"

EMAIL = "johny@bull.com"

EMAILAA = "aaaa@bull.com"


class MixinTest(RequestMixin):

    def _getlist(self, meth) -> list[dict]:
        r = self.getrequest(meth)
        return r['res']

    def _getusers(self) -> list[dict]:
        return self._getlist("users/list")

    def _gettrips(self) -> list[dict]:
        return self._getlist("trips/list")

    def _gettransportation(self, tripid: int) -> list[dict]:
        r = self.getrequest("transportation/list", par1='trip_id', val1=tripid)
        return r['res']

    def _getflight(self, tripid: int) -> list[dict]:
        r = self.getrequest("flight/list", par1='trip_id', val1=tripid)
        return r['res']

    def _getstays(self, tripid: int) -> list[dict]:
        r = self.getrequest("stays/list", par1='trip_id', val1=tripid)
        return r['res']
    
    def _getevents(self, tripid: int) -> list[dict]:
        r = self.getrequest("trips/liste", par1='trip_id', val1=tripid)
        return r['res']

    # ------------------
    # user action
    # ------------------

    def _usersaction(self, what: str, data: dict):
        return self.putwhatrequest("users/action", what, data)

    def _usersactiondel(self, pk: int):
        return self.delrequestwhat("users/action", "delete", "pk", pk)

    # -----------------
    # trips action
    # -----------------

    def _tripsaction(self, what: str, data: dict):
        return self.putwhatrequest("trips/action", what, data)

    def _tripsactiondel(self, pk: int):
        return self.delrequestwhat("trips/action", "delete", "pk", pk)

    def _participantsaction(self, what: str, data: dict):
        return self.putwhatrequest("trips/participantsaction", what, data)

    # ---------------
    # trips helpers
    # ---------------

    @pytest.fixture(autouse=True)
    def del_trips(self):
        trips = self._get_test_trips()
        for t in trips:
            pk = t['pk_trips']
            r = self._tripsactiondel(pk)
            print(r)
        use = self._get_test_trips()
        assert (0 == len(use))

    def _get_test_trips(self) -> list[dict]:
        trips: list[dict] = self._gettrips()
        return [u for u in trips if u['name'] == TESTNAME]

    def _get_trip(self) -> dict:
        trips = self._get_test_trips()
        assert (1 == len(trips))
        return trips[0]

    def _add_trip(self) -> dict:
        data = {
            "name": TESTNAME
        }
        r = self._tripsaction("add", data)
        print(r)
        trips = self._get_test_trips()
        assert (1 == len(trips))
        return trips[0]

    # -------------
    # user helpers
    # -------------

    @pytest.fixture(autouse=True)
    def del_users(self):
        use = self._get_test_users()
        for u in use:
            pk = u['pk_users']
            r = self._usersactiondel(pk)
            print(r)
        use = self._get_test_users()
        assert (0 == len(use))

    def _get_test_users(self) -> list[dict]:
        use: list[dict] = self._getusers()
        return [u for u in use if u['email'] == EMAIL or u['email'] == EMAILAA]

    def _add_testuser(self) -> dict:
        data: dict = {
            "name": "John",
            "email": EMAIL
        }
        r = self._usersaction("add", data)
        print(r)
        use = self._get_test_users()
        assert (1 == len(use))
        return use[0]

    # -------------------------
    # transportation actions
    # -------------------------

    def _transportationaction(self, what: str, data: dict):
        return self.putwhatrequest("transportation/action", what, data)

    def _transportationactiondel(self, pk: int):
        return self.delrequestwhat("transportation/action", "delete", "pk", pk)

    # ----------------
    # flight action
    # ----------------

    def _flightaction(self, what: str, data: dict):
        return self.putwhatrequest("flight/action", what, data)

    def _flightactiondel(self, pk: int):
        return self.delrequestwhat("flight/action", "delete", "pk", pk)

    # ----------------
    # stays action
    # ----------------

    def _staysaction(self, what: str, data: dict):
        return self.putwhatrequest("stays/action", what, data)

    def _staysactiondel(self, pk: int):
        return self.delrequestwhat("stays/action", "delete", "pk", pk)

    # -------------
    # helpers
    # -------------

    @staticmethod
    def assertDate(validT: str, r: dict, k: str):
        d: str = r[k]
        assert (validT == d[:10])
