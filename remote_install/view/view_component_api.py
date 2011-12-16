#
# view_component_api.py:
#   Parameterized functions to handle rendering HTML to view components
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


from remote_install.models.user import User
from remote_install.models.installer import Installer
from remote_install.models.machine import MachineTemplate, Machine, MachineSlot
from remote_install import app
from sqlalchemy import desc
from flask.views import MethodView
from flask import render_template

class BaseViewApi(MethodView):
    per_page = 10

    def get_template(self):
        raise NotImplementedError()

    def get_objects(self, page):
        raise NotImplementedError()

    def get_name(self):
        raise NotImplementedError()

    def get(self, page):
        if app.debug:
            app.logger.debug('rendering page %d for show_%s' % (page, self.get_name()))

        return render_template(self.get_template(), name= self.get_name(),
                                paginate= self.get_objects(page))

class ViewUserApi(BaseViewApi):
    def get_template(self):
        return 'view/view_users.html'

    def get_objects(self, page):
        return User.query.order_by(desc('id')).paginate(page, self.per_page)

    def get_name(self):
        return "User"

class ViewMachineTemplateApi(BaseViewApi):
    def get_template(self):
        return 'view/view_machine_templates.html'

    def get_objects(self, page):
        return MachineTemplate.query.order_by(desc('id')).paginate(page, self.per_page)

    def get_name(self):
        return "Machine Template"

class ViewInstallerApi(BaseViewApi):
    # installer view takes up more space, do fewer per page
    per_page = 5

    def get_template(self):
        return 'view/view_installers.html'

    def get_objects(self, page):
        return Installer.query.order_by(desc('id')).paginate(page, self.per_page)

    def get_name(self):
        return "Installer"

class ViewMachineApi(BaseViewApi):
    def get_template(self):
        return 'view/view_machines.html'

    def get_objects(self, page):
        return Machine.query.order_by(desc('id')).paginate(page, self.per_page)

    def get_name(self):
        return "Machine"

class ViewMachineSlotApi(BaseViewApi):
    def get_template(self):
        return 'view/view_machine_slots.html'

    def get_objects(self, page):
        return MachineSlot.query.order_by(desc('id')).paginate(page, self.per_page)

    def get_name(self):
        return "Machine Slot"

