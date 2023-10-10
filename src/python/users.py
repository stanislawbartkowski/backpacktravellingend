from tools.crudop import CRUOP
from tools.helper import postdispatch


class USERS(CRUOP):

    _TABLE = 'users'
    _COLS = ['name', 'email', 'phone_number', 'description']
    _COLTODUPLICATE = 'email'
    _DELNOTIFICATION: str = "User deleted"
    _UPDATENOTIFICATION: str = "User data updated"
    _ADDNOTIFICAITON: str = "New user added"


@postdispatch(cols=USERS._COLS)
def _actions(d):
    U = USERS()
    U.registerwhat(d)


if __name__ == "__main__":
    _actions()
