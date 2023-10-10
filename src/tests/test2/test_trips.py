from testmixin import TESTNAME, MixinTest


_STARTTIME = "2023-05-15"
_ENDTIME = "2023-05-22"


class TestTrip(MixinTest):

    # -----------------
    # tests
    # ----------------

    def test_add(self, del_trips):
        self._add_trip()

    def test_add_dates(self, del_trips):
        data = {
            "name": TESTNAME,
            "tripdate": [_STARTTIME, _ENDTIME]
        }
        r = self._tripsaction("add", data)
        print(r)
        trip: dict = self._get_trip()
        print(trip)
        self.assertDate(_STARTTIME, trip, "start_time")
        self.assertDate(_ENDTIME, trip, "end_time")

    def test_participants(self, del_trips, del_users):
        self._add_testuser()
        data = {
            "name": TESTNAME
        }
        r = self._tripsaction("add", data)
        print(r)
        trip = self._get_trip()
        r = self._participantsaction('initparticipants', trip)
        print(r)

        use: list[dict] = self._getusers()
        user: dict = use[0]
        pk_user = user['pk_users']
        participants = [pk_user]
        trip["participants"] = participants
        r = self._participantsaction('updateparticipants', trip)
        print(r)

        r = self._participantsaction('initparticipants', trip)
        print(r)
        nparticipants = r["participants"]
        print(nparticipants)
        assert (participants == nparticipants)
