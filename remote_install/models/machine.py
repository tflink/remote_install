#
# machine.py - SQLAlchemy declaration for machine related data
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

class MachineTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    memory = db.Column(db.Integer)
    disk = db.Column(db.Integer)

    def __init__(self, name, memory, disk):
        self.name = name
        self.memory = memory
        self.disk = disk

    def __repr__(self):
        return '<MachineTemplate %r>' % self.name

    @classmethod
    def from_form_data(cls, form):
        return cls(form['template_name'], form['memory'], form['disk'])

class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('machine_template.id'))
    template = db.relationship('MachineTemplate', backref = db.backref('machines', lazy='dynamic'))
    name = db.Column(db.String(80), unique=False)
    installer_id = db.Column(db.Integer, db.ForeignKey('installer.id'))
    installer = db.relationship('Installer', backref = db.backref('machines', lazy='dynamic'))
    status = db.Column(db.String(80), unique=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('machine_slot.id'))
    slot = db.relationship('MachineSlot', backref = db.backref('machine', lazy='dynamic'))

    def __init__(self, name, template, installer, status, slot):
        self.name = name
        self.template = template
        self.installer = installer
        self.status = status
        self.slot = slot

    def __repr__(self):
        return '<Machine %r>' % self.name

class MachineSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    macaddress = db.Column(db.String(80), unique=False)
    url = db.Column(db.String(120), unique=False)
    username = db.Column(db.String(80), unique=False)
    password = db.Column(db.String(80), unique=False)
    active = db.Column(db.Boolean)

    def __init__(self, macaddress, url, username, password):
        self.macaddress = macaddress
        self.url = url
        self.username = username
        self.password = password
        self.active = False

    def __repr__(self):
        return '<MachineSlot %r>' % self.macaddress

    @classmethod
    def from_form_data(cls, form):
        return cls(form['macaddress'], form['url'], form['username'], form['password'])
