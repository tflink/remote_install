#
# installer.py - SQLAlchemy declaration for installer data
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
import datetime

class Installer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    fedora_version = db.Column(db.Integer)
    version = db.Column(db.String(80))
    location = db.Column(db.String(120))
    media_type = db.Column(db.String(80))
    creation_date = db.Column(db.DateTime)

    def __init__(self, name, fedora_version, version, location, media_type,
                       creation_date):
        self.name = name
        self.fedora_version = fedora_version
        self.version = version
        self.location = location
        self.media_type = media_type
        self.creation_date = creation_date

    def __repr__(self):
        return '<Installer %r %r>' % (self.name, self.version)

    @classmethod
    def from_form_data(cls, form):
        return cls(form['installer_name'], int(form['fedora_version']),
                   form['version'], form['location'], form['installer_type'],
                   datetime.datetime.now())
