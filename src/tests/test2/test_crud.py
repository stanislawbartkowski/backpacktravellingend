from typing import List

from testmixin import EMAIL, EMAILAA, MixinTest


class TestCRUD(MixinTest):

    def test_add(self, del_users):
        self._add_testuser()

    def test_duplicated(self, del_users):
        data: dict = {
            "name": "John",
            "email": EMAIL,
            "currentfield": EMAIL
        }
        r = self._usersaction("duplicatedvalue", data)
        print(r)
        assert ('err' not in r)

        r = self._usersaction("add", data)
        print(r)
        r = self._usersaction("duplicatedvalue", data)
        print(r)
        assert ('err' in r)

    def test_duplicatedupdate(self, del_users):
        data: dict = {
            "name": "John",
            "email": EMAIL,
        }
        r = self._usersaction("add", data)
        print(r)
        use = self._get_test_users()
        assert (1 == len(use))
        data = use[0]
        data["currentfield"] = EMAIL
        r = self._usersaction("duplicatedvalue", data)
        print(r)
        assert ('err' not in r)

        # add another
        data: dict = {
            "name": "John",
            "email": EMAILAA,
        }
        r = self._usersaction("add", data)
        print(r)
        use = self._get_test_users()
        assert (2 == len(use))
        useraa = next(f for f in use if f['email'] == EMAILAA)

        # try change email to _EMAIL
        useraa["currentfield"] = EMAIL
        r = self._usersaction("duplicatedvalue", useraa)
        print(r)
        assert ('err' in r)

    def test_update(self, del_users):
        data: dict = {
            "name": "John",
            "email": EMAIL,
        }
        r = self._usersaction("add", data)
        print(r)
        use = self._get_test_users()
        assert (1 == len(use))
        data = use[0]
        data["phone_number"] = '1111-2222-3333'
        r = self._usersaction("update", data)
        print(r)
        use = self._get_test_users()
        assert (1 == len(use))
        data = use[0]
        assert (data["phone_number"] == '1111-2222-3333')

    def test_delete(self, del_users):
        data: dict = {
            "name": "John",
            "email": EMAIL,
        }
        r = self._usersaction("add", data)
        print(r)
        use = self._get_test_users()
        assert (1 == len(use))

        data = use[0]
        r = self._usersactiondel(data["pk_users"])
        print(r)
        use = self._get_test_users()
        assert (0 == len(use))
