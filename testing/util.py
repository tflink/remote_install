import datetime
from remote_install.models.installer import Installer
from remote_install.models.machine import MachineTemplate, Machine, MachineSlot
from remote_install.models.user import User


def get_test_user():
    return User('bill', 'bill@test.me')


def get_test_machine(template, installer, slot):
    return Machine('test-1', template, installer, 'RUNNING', slot)


def get_test_slot():
    return MachineSlot('01:23:45:67:89:0A', 'http://localhost:8080/guacamole',
                        'username', 'password')


def get_test_template():
    return MachineTemplate('test template 1', 1024, 10)


def get_test_installer():
    return Installer('test installer', 99, '1.0', '/srv/test.iso', 'iso',
                        datetime.datetime.now())


def prime_db(db):
    user = get_test_user()
    template = get_test_template()
    installer = get_test_installer()
    slot = get_test_slot()

    db.session.add(user)
    db.session.add(template)
    db.session.add(installer)
    db.session.add(slot)
    db.session.commit()

