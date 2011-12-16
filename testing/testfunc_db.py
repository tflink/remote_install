import pytest
import datetime

from remote_install import db
from remote_install.models.user import User
from remote_install.models.installer import Installer
from remote_install.models.machine import MachineTemplate, Machine, MachineSlot
from remote_install.models.job import Job
import testing.util


# utility functions for populating other models
class TestFuncDb():

    def setup_method(self, method):
        db.drop_all()
        db.create_all()

    def test_add_single_user(self):
        ref_username = 'bill'
        ref_email = 'bill@users.com'
        test_user = User(ref_username, ref_email)

        db.session.add(test_user)
        db.session.commit()

        test_users = User.query.all()

        assert len(test_users) == 1
        assert test_users[0].username == ref_username
        assert test_users[0].email == ref_email

    def test_add_single_installer(self):
        ref_name = "Test Installer"
        ref_fedora_version = 99
        ref_version = "1.0"
        ref_location = "http://somewhere/isos/fedora.iso"
        ref_media_type = "iso"
        ref_creation_date = datetime.datetime.now()

        ref_installer = Installer(ref_name, ref_fedora_version, ref_version,
                                   ref_location, ref_media_type,
                                   ref_creation_date)

        db.session.add(ref_installer)
        db.session.commit()

        test_installers = Installer.query.all()

        assert len(test_installers) == 1

        test_installer = test_installers[0]
        assert test_installer.name == ref_name
        assert test_installer.fedora_version == ref_fedora_version
        assert test_installer.version == ref_version
        assert test_installer.location == ref_location
        assert test_installer.media_type == ref_media_type
        assert test_installer.creation_date == ref_creation_date

    def test_add_single_machine_template(self):
        ref_name = 'test machine 1'
        ref_memory = 1024
        ref_disk = 10

        ref_template = MachineTemplate(ref_name, ref_memory, ref_disk)

        db.session.add(ref_template)
        db.session.commit()

        test_templates = MachineTemplate.query.all()

        assert len(test_templates) == 1

        assert test_templates[0].name == ref_name
        assert test_templates[0].memory == ref_memory
        assert test_templates[0].disk == ref_disk

    def test_add_single_machine_slot(self):
        ref_mac = '01:23:45:67:89:0A'
        ref_url = 'http://localhost:8080/guacamole'
        ref_username = 'username'
        ref_password = 'password'

        ref_slot = MachineSlot(ref_mac, ref_url, ref_username, ref_password)

        db.session.add(ref_slot)
        db.session.commit()

        test_slots = MachineSlot.query.all()

        assert len(test_slots) == 1

        assert test_slots[0].macaddress == ref_mac
        assert test_slots[0].url == ref_url
        assert test_slots[0].username == ref_username
        assert test_slots[0].password == ref_password

    def test_add_single_machine(self):
        ref_name = 'test1'
        ref_status = 'RUNNING'

        ref_template = testing.util.get_test_template()
        ref_installer = testing.util.get_test_installer()
        ref_slot = testing.util.get_test_slot()

        ref_machine = Machine(ref_name, ref_template, ref_installer,
                                ref_status, ref_slot)

        db.session.add(ref_template)
        db.session.add(ref_installer)
        db.session.add(ref_machine)
        db.session.commit()

        test_machines = Machine.query.all()

        assert len(test_machines) == 1
        assert test_machines[0].name == ref_name
        assert test_machines[0].status  == ref_status
        assert test_machines[0].template == ref_template
        assert test_machines[0].installer == ref_installer
        assert test_machines[0].slot  == ref_slot

    def test_add_single_job(self):
        ref_name = 'test job 1'
        ref_status = 'QUEUED'

        ref_user = testing.util.get_test_user()
        ref_machine = testing.util.get_test_machine(testing.util.get_test_template(),
                        testing.util.get_test_installer(), testing.util.get_test_slot())

        ref_job = Job(ref_name, ref_user, ref_status, ref_machine)

        db.session.add(ref_user)
        db.session.add(ref_machine)
        db.session.add(ref_job)
        db.session.commit()

        test_jobs = Job.query.all()

        assert len(test_jobs) == 1
        assert test_jobs[0].name == ref_name
        assert test_jobs[0].status == ref_status
        assert test_jobs[0].user == ref_user
        assert test_jobs[0].machine == ref_machine
