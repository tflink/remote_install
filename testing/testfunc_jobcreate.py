from remote_install import db, app
import testing.util
from remote_install.models.user import User
from remote_install.models.installer import Installer
from remote_install.models.machine import MachineTemplate, Machine
from remote_install.models.job import Job
from remote_install.machine_control.stub import StubMachineControl
import os

test_app = app.test_client()


machine_control = StubMachineControl()

def get_machine_control():
    return machine_control

class TestFuncJobcreate():

    @classmethod
    def setup_class(cls):
        db.create_all()
        testing.util.prime_db(db)

    @classmethod
    def teardown_class(cls):
        db.drop_all()

    def setup_method(self, method):
        self.app = app.test_client()

    def test_is_testing(self):
        assert os.getenv('TEST') == 'yes'
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite://'

    def test_create_machine(self):
        ref_user = User.query.first()
        ref_template = MachineTemplate.query.first()
        ref_installer = Installer.query.first()

        ref_data = {'user': ref_user.id, 'installer':ref_installer.id,
                'template':ref_template.id}

        rv = self.app.post('/job/new', data=ref_data)

        # check to see if we are being redirected
        assert 'Redirecting' in rv.data
        print rv.data

        # check to see if the db entries were added correctly
        ref_user = User.query.first()
        ref_template = MachineTemplate.query.first()
        test_machine= Machine.query.first()
        test_job = Job.query.first()

        assert test_job.user == ref_user
        assert test_job.machine == test_machine
        assert test_machine.template == ref_template


#    def test_create_machine_backend(self, monkeypatch):
#        ref_user = User.query.first()
#        ref_template = MachineTemplate.query.first()
#        ref_installer = Installer.query.first()
#
#        ref_data = {'user': ref_user.id, 'installer':ref_installer.id,
#                'template':ref_template.id}
#        monkeypatch.setattr(app.blueprints['frontend'],
#                            'get_machine_control', get_machine_control)
#
#        rv = self.app.post('/job/new', data=ref_data)
#
#        assert len(machine_control.machines) == 1

