#!/bin/python

# This is a VERY quick and dirty way to initialize what needs to be setup
# to get remote_install to run.
# IT WILL DELETE YOUR CURRENT DATABASE!!
# be careful when you use it.

from remote_install.models.user import User
from remote_install import db

if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    user = User('admin', 'password', 'admin@localhost', is_admin=True)
    db.session.add(user)
    db.session.commit()


