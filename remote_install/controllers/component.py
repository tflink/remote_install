#
# component.py - Interface to add and edit most of the "components"
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


from flask import Blueprint, request, render_template, url_for, redirect, flash
from flaskext.login import current_user
from remote_install import app, db
from remote_install.view.create_component_api import CreateInstallerApi, CreateUserApi, CreateMachineTemplateApi, CreateMachineSlotApi
from remote_install.view.view_component_api import ViewUserApi, ViewMachineTemplateApi, ViewInstallerApi, ViewMachineApi, ViewMachineSlotApi
from remote_install.models.machine import Machine
from remote_install.models.user import User

import remote_install.controllers.job

component = Blueprint('component', __name__)

@component.before_request
def restrict_components_to_users():
    if not current_user.is_authenticated():
        return app.login_manager.unauthorized()

@component.route('/')
def index():
    if app.debug:
        app.logger.debug('rendering index')
    return render_template('main.html')

# endpoints for creating new components
component.add_url_rule('/component/installer/new', 'new_installer',
                        view_func=CreateInstallerApi.as_view('installer'))
component.add_url_rule('/component/machine_template/new', 'new_machine_template',
                        view_func=CreateMachineTemplateApi.as_view('machine_template'))
component.add_url_rule('/component/user/new', 'new_user',
                        view_func=CreateUserApi.as_view('user'))
component.add_url_rule('/component/machine_slot/new', 'new_machine_slot',
                        view_func=CreateMachineSlotApi.as_view('machine_slot'))

# this consolidates the paging boilerplate for the view functions into a single
# function
def register_view_api(view, endpoint, url, pk='id', pk_type='int', default=None):
    view_func = view.as_view(endpoint)
    component.add_url_rule(url, defaults={pk:default}, view_func = view_func,
                            methods=['GET'])
    component.add_url_rule('%spage/<%s:%s>' %(url, pk_type, pk),
                            view_func=view_func,methods=['GET'])

# endpoints for the view functions
register_view_api(ViewUserApi, 'show_users', '/component/user/', pk='page', default=1)
register_view_api(ViewMachineTemplateApi, 'show_machine_templates',
                    '/component/machine_template/', pk='page', default=1)
register_view_api(ViewInstallerApi, 'show_installers', '/component/installer/',
                    pk='page', default=1)
register_view_api(ViewMachineApi, 'show_machines', '/component/machine/', pk='page', default=1)
register_view_api(ViewMachineSlotApi, 'show_machine_slots',
                    '/component/machine_slot/', pk='page', default=1)

@component.route('/component/user/<int:user_id>', methods = ['POST'])
def process_user(user_id):
    if not current_user.admin:
        flash('You need admin priviliges to make changes')
        return redirect(url_for('.show_users'))

    user = User.query.get(user_id)
    if user and request.form['request']:
        if request.form['request'] == 'MAKE_ADMIN':
            user.admin = True
        elif request.form['request'] == 'REMOVE_ADMIN':
            user.admin = False
        else:
            flash('Invalid Request: %s' % request.form['request'])
            redirect(url_for('.show_users'))
        db.session.add(user)
        db.session.commit()
        flash('Request %s for user %s Succeeded.' % (request.form['request'], user.username))
        return redirect(url_for('.show_users'))

@component.route('/component/machine/<int:machine_id>', methods = ['GET', 'POST'])
def machine_detail(machine_id):
    if request.method == 'GET':
        if app.debug:
            app.logger.debug('rendering detail for machine %d' % machine_id)

        machine = Machine.query.get_or_404(machine_id)
        return render_template('detail_machine.html', machine = machine)

    if request.method == 'POST':
        if app.debug:
            app.logger.debug('machine %d received POST request %s' % (machine_id, str(request.form)))

        if request.form['request']:
            if request.form['request'] == 'STOP':
                app.logger.info('Stopping machine %d' % machine_id)
                machine = Machine.query.filter_by(id=machine_id).first()

                machine_control = remote_install.controllers.job.get_machine_control()
                machine_control.stop_machine(machine.name)

                machine.status = 'STOPPED'
                db.session.add(machine)
                db.session.commit()

            if request.form['request'] == 'DELETE':
                app.logger.info('Deleting machine %d' % machine_id)
                machine = Machine.query.filter_by(id=machine_id).first()

                machine_control = remote_install.controllers.job.get_machine_control()
                machine_control.delete_machine(machine.name)
                machine_control.delete_disk(machine.name)

                machine.status = 'DELETED'
                db.session.add(machine)
                db.session.commit()

        return render_template('detail_machine.html', machine = machine)

