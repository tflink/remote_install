#
# main.py - interface for login, logout and the main page
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


from remote_install import app, db, login_manager
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flaskext.login import login_user, logout_user, login_required, current_user, AnonymousUser
import datetime

from remote_install.models.user import User

main = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(userid):
    user = User.query.get(userid)
    if user:
        return user
    else:
        return AnonymousUser

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            # refresh last auth time since it's used to check login
            user.lastauth = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            login_user(user)

            app.logger.info('Successful login for user %s' % request.form['username'])
            flash('Logged In Successfully!')
            return redirect(request.args.get('next') or url_for('.index'))
        else:
            app.logger.info('FAILED login for user %s' % request.form['username'])
            flash('Login Failed! Please Try again!')
            return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    current_user.lastauth = None
    db.session.add(current_user)
    db.session.commit()
    logout_user()
    return redirect(url_for('.index'))

@main.route('/')
def index():
    if app.debug:
        app.logger.debug('rendering index')
    return render_template('main.html')

