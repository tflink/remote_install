#
# create_component_api.py:
#   Parameterized functions to handle rendering HTML forms to gather data for
#   components and processing that data into database entried
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


from remote_install.view import BaseApi
from remote_install.models.user import User
from remote_install.models.installer import Installer
from remote_install.models.machine import MachineTemplate, MachineSlot
from flask import request, url_for, redirect
from remote_install import db, app

class CreateInstallerApi(BaseApi):
    def get_new_template(self):
        return 'create/create_installer.html'

    def get_name(self):
        return "Installer"

    def get_action_name(self):
        return "installer"

    def post(self):
        app.logger.debug('installer form: %s' % str(request.form))
        installer = Installer.from_form_data(request.form)
        db.session.add(installer)
        db.session.commit()
        app.logger.debug('making debug message from user api')
        return redirect(url_for('.index'))


class CreateMachineTemplateApi(BaseApi):
    def get_new_template(self):
        return 'create/create_machine_template.html'

    def get_name(self):
        return "Machine Template"

    def get_action_name(self):
        return "machine_template"

    def post(self):
        app.logger.debug('machine template form: %s' % str(request.form))
        template = MachineTemplate.from_form_data(request.form)
        db.session.add(template)
        db.session.commit()
        return redirect(url_for('.index'))


class CreateUserApi(BaseApi):
    def get_new_template(self):
        return 'create/create_user.html'

    def get_name(self):
        return "User"

    def get_action_name(self):
        return "user"

    def post(self):
        app.logger.debug('user form: %s' % str(request.form))
        user = User.from_form_data(request.form)
        db.session.add(user)
        db.session.commit()
        app.logger.debug('making debug message from user api')
        return redirect(url_for('.index'))


class CreateMachineSlotApi(BaseApi):
    def get_new_template(self):
        return 'create/create_machine_slot.html'

    def get_name(self):
        return "Machine Slot"

    def get_action_name(self):
        return "machine_slot"

    def post(self):
        app.logger.debug('machine_slot form: %s' % str(request.form))
        slot = MachineSlot.from_form_data(request.form)
        db.session.add(slot)
        db.session.commit()
        app.logger.debug('making debug message from machine slot api')
        return redirect(url_for('.index'))
