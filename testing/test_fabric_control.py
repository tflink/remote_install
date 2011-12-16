from remote_install.machine_control import FabricController

class TestFabricControl():

    def setup_method(self, method):
        self.test_control = FabricController()

    def test_make_install_cmd(self):
        ref_name = 'test1'
        ref_disk = 'disk1'
        ref_memory = 1024
        ref_location = '/dev/iso'
        ref_macaddress = '01:23:45:67:89:AB'

        test_cmd = self.test_control.make_install_cmd(ref_name, ref_disk,
                        ref_memory, ref_location, ref_macaddress)

        assert len(test_cmd) > 0
