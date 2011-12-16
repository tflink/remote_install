#
# user.py - SQLAlchemy declaration for user data
#
# Copyright 2011, Red Hat, Inc
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Authors:
#   Tim Flink <tflink@redhat.com>


from remote_install import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class User(db.Model):

    # for now, do a session expire after 2 hours
    login_maxinactive = datetime.timedelta(hours=2)

    # stuff that's persisted
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String(160), unique=False)
    admin = db.Column(db.Boolean())
    lastauth = db.Column(db.DateTime)
    lastactive = db.Column(db.DateTime)


    def __init__(self, username, password, email, is_admin=False):
        self.username = username
        self.email = email
        self.admin = is_admin
        self.set_password(password)
        self.lastauth = None
        self.lastactive = None

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def get_id(self):
        return self.id

    def is_authenticated(self):
        if not self.lastauth:
            return False
        if (datetime.datetime.now() - self.lastauth) > self.login_maxinactive:
            return False
        else:
            return True

    def is_active(self):
        return self.is_authenticated()

    def is_anonymous(self):
        return False

    @classmethod
    def from_form_data(cls, form):
        if 'is_admin' in form.keys() and form['is_admin'] == "True":
            is_admin = True
        else:
            is_admin = False
        return cls(form['username'], form['password'], form['user_email'], is_admin)
