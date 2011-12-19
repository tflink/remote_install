#
# job.py - interface for creating, viewing and changing job-related data
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


from flask import Blueprint, render_template, request, redirect, url_for, flash
from flaskext.login import login_required, current_user
from sqlalchemy import desc
from remote_install.models.job import Job
from remote_install import db, app
import os
from remote_install.machine_control import FabricController
from remote_install.machine_control.stub import StubMachineControl
from remote_install.models.installer import Installer
from remote_install.models.machine import MachineTemplate, Machine, MachineSlot
from remote_install.models.user import User

jobs = Blueprint('job', __name__)

@jobs.route('/job/', defaults={'page': 1})
@jobs.route('/job/page/<int:page>', methods = ['GET'])
def show_jobs(page):
    job_paginate = Job.query.order_by(desc('id')).paginate(page, per_page=10)
    return render_template('view/view_jobs.html', paginate = job_paginate)


@jobs.route('/job/mine', defaults={'page': 1})
@jobs.route('/job/mine/page/<int:page>', methods = ['GET'])
@login_required
def show_my_jobs(page):
    job_paginate = Job.query.filter_by(user=current_user).order_by(desc('id')).paginate(page, per_page=10)
    return render_template('view/view_jobs.html', paginate = job_paginate)

@jobs.route('/job/new', methods = ['GET', 'POST'])
@login_required
def new_job():
    if request.method == 'GET':
        slots = MachineSlot.query.filter_by(active=False).all()
        if not len(slots) > 0:
            app.logger.info('All slots are currently full')
            flash('No slots are currently available, please try again later')
            return redirect(url_for('main.index'))
        else:
            app.logger.info('There are currently %d slots available' % len(slots))
            flash('There are currently %d slots available' % len(slots))

        users = User.query.all()
        templates = MachineTemplate.query.all()
        installers = Installer.query.all()
        return render_template('create/create_job.html', users=users, templates=templates, installers=installers)

    elif request.method == 'POST':
        slots = MachineSlot.query.filter_by(active=False).all()
        if not len(slots) > 0:
            app.logger.info('All slots are currently full')
            flash('No slots are currently available, please try again later')
            return redirect(url_for('main.index'))

        # grab data out of the POST form
        template = MachineTemplate.query.filter(MachineTemplate.id == request.form['template']).first()
        installer = Installer.query.filter(Installer.id == request.form['installer']).first()

        # setup slot and job
        if app.debug:
            app.logger.debug('Reserving slot %d and creating skeleton job' % slots[0].id)

        slot = slots[0]
        slot.active = True

        job = Job('newjob', current_user, 'INITIALIZING', None)
        db.session.add(slot)
        db.session.add(job)
        db.session.commit()

        if app.debug:
            app.logger.debug('Skeleton job %d created ' % job.id)


        machine_name = 'test-%d' % job.id
        machine = Machine(machine_name, template, installer, 'INIT', slot)

        job.machine = machine
        job.name = "job-%d" % job.id
        db.session.add(machine)
        db.session.add(job)
        db.session.commit()

        app.logger.info('Creating new virtual machine for job %d' % job.id)

        # create the machine
        machine_control = get_machine_control()
        kickstart = 'http://%s:%d/job/%d/kickstart' % \
                    (app.config['KICKSTART_SERVER'],
                        app.config['KICKSTART_PORT'], job.id)
        if app.debug:
            app.logger.debug('creating new machine %s' % machine_name)

        logs =  machine_control.create_machine(machine_name,
                                    template,installer, slot, kickstart)

        # finish up the metadata
        app.logger.info('Machine %s created' % machine.name)

        machine.status = 'RUNNING'
        db.session.add(machine)
        db.session.commit()

        return redirect(url_for('.job_detail', job_id=job.id))


def get_machine_control():
    if os.getenv('TEST') == 'yes' or app.config['FAKE_MACHINE'] == True:
        return StubMachineControl()
    else:
        return FabricController()


@jobs.route('/job/<int:job_id>', methods = ['GET', 'POST'])
def job_detail(job_id):

    job = Job.query.get_or_404(job_id)
    if job.status == 'INITIALIZING':
        flash('The job has been created and is currently initializing. Once ' \
                'initialization is complete, this page will show login information. ' \
                'Please wait about 30 seconds and refresh the page manually.')

    if request.method == 'GET':
        if app.debug:
            app.logger.debug('rendering detail for job %d' % job_id)

        log_files = []
        try:
            log_files = os.listdir('%s/test-%d' % (app.config['LOG_LOCATION'], job.id))
        except OSError:
            app.logger.warn('No logs found for job %d' % job.id)

        # if the job isn't running, don't bother getting the slot information
        slot = None
        if job.status in ['RUNNING', 'INSTALLING']:
            slot = job.machine.slot

        return render_template('detail_job.html', job = job,
                                log_prefix = app.config['LOG_PREFIX'],
                                logs = log_files, slot=slot)

    if request.method == 'POST':
        if not (current_user.admin or current_user.get_id() == job.user.id):
            app.logger.warn('User %s (id: %d) tried to modify job %d (owner: %s, id: %d)' %
                    (current_user.username, current_user.get_id(), job.id, job.user.username, job.user.id))
            flash('You need admin priviliges to make changes to this job.')
            return redirect(url_for('job.job_detail', job_id=job_id))

        if app.debug:
            app.logger.debug('job %d received POST request %s' % (job_id, str(request.form)))

        if request.form['request']:
            machine_control = get_machine_control()

            if request.form['request'] == 'COMPLETE':
                app.logger.info('Completing job %d' % job_id)
                job.status = 'COMPLETE'
                job.machine.slot.active = False

                # now shutdown and delete the VM
                if job.machine.status not in ['STOPPED', 'DELETED']:
                    machine_control.stop_machine(job.machine.name)
                    job.machine.status = 'STOPPED'
                if job.machine.status != 'DELETED':
                    machine_control.delete_machine(job.machine.name)
                    machine_control.delete_disk(job.machine.name)
                    job.machine.status = 'DELETED'

                db.session.add(job)
                db.session.add(job.machine.slot)
                db.session.add(job.machine)
                db.session.commit()

            if request.form['request'] == 'RESTART':
                machine_control.start_machine(job.machine.name)
                job.machine.status = 'RUNNING'
                db.session.add(job.machine)
                db.session.commit()


        return redirect(url_for('.job_detail', job_id=job_id))


@jobs.route('/job/<int:job_id>/init_done', methods = ['GET'])
def complete_job_init(job_id):
    job = Job.query.get(job_id)
    job.status = 'INSTALLING'
    db.session.add(job)
    db.session.commit()
    return "OK"


@jobs.route('/job/<int:job_id>/install_done', methods = ['GET'])
def complete_job_installing(job_id):
    job = Job.query.get(job_id)
    job.status = 'RUNNING'

    # one artifact of using virt-install is that it doesn't allow for restarting
    # after anaconda is done, QND fix is to mark the machine stopped and allow
    # for manual restarting

    job.machine.status = 'STOPPED'
    db.session.add(job)
    db.session.add(job.machine)
    db.session.commit()
    return "OK"


@jobs.route('/job/<int:job_id>/kickstart', methods = ['GET'])
def get_kickstart(job_id):
    job = Job.query.get(job_id)
    server = app.config['KICKSTART_SERVER']
    port = app.config['KICKSTART_PORT']
    password = job.machine.slot.password
    tree = job.machine.installer.location
    job_num = job.id
    return render_template('kickstart/base.ks', password=password, tree=tree,
                            job_num = job_num, server=server, port=port)
