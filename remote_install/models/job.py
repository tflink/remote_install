#
# job.py - SQLAlchemy declaration for job data
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

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref = db.backref('jobs', lazy='dynamic'))
    status = db.Column(db.String(80), unique=False)
    name = db.Column(db.String(80), unique=False)
    machine_id = db.Column(db.Integer, db.ForeignKey('machine.id'))
    machine = db.relationship('Machine', backref=db.backref('jobs', lazy='dynamic'))

    def __init__(self, name, user, status, machine):
        self.name = name
        self.user = user
        self.status = status
        self.machine = machine

    def __repr__(self):
        return '<Job %r for %r>' % (self.name, self.user)
