from testmixin import MixinTest


class TestHealth(MixinTest):
    
    def test_version(self):
        r = self.getrequest("restversion")
        assert ("restver" in r)

    def test_healthconnection(self):
        r = self.getrequest("healthcheck", "checkconnection")
        print(r)
        assert ("OK" == r["res"])
