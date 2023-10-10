
import functools
import requests

# _URL = "http://localhost:7999"
_HEADERS = {}


def _getwhatpars(what: str, par1: str = None, val1=None) -> dict:
    pars = {} if what is None else {'what': what}
    if par1 is None:
        return pars
    pars[par1] = val1
    return pars


class RequestMixin:

    url: str

    def _request(func):
        @functools.wraps(func)
        def func_wrapper(self, *args, **kwargs):
            r = func(self, *args, **kwargs)
            assert (r.status_code == 200)
            return r.json()
        return func_wrapper

    @_request
    def getrequest(self, meth, what: str = None, par1: str = None, val1: str = None):
        return requests.get(f"{self.url}/{meth}", headers=_HEADERS, params=_getwhatpars(what, par1, val1))

    @_request
    def putwhatrequest(self, meth, what: str, data: dict):
        return requests.post(f"{self.url}/{meth}", headers=_HEADERS, params=_getwhatpars(what), json=data)

    @_request
    def delrequest(self, meth, par1=None, val1=None):
        return requests.delete(f"{self.url}/{meth}", headers=_HEADERS, params=_getwhatpars(None, par1, val1))

    @_request
    def delrequestwhat(self, meth, what: str, par1=None, val1=None):
        return requests.delete(f"{self.url}/{meth}", headers=_HEADERS, params=_getwhatpars(what, par1, val1))
