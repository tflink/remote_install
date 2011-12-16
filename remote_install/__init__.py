#!/usr/bin/env python

#
# remote_install
#   sets up the application and chooses configuration options based on
#   environment variables
#
# Copyright 2010,2011 Red Hat, Inc and others
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
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


# This borrows very heavily from flask-boilerplate for application structure
# and configuration methods

import os
from flaskext.sqlalchemy import SQLAlchemy
from flaskext.login import LoginManager

FLASK_APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Flask
from flask import Flask
app = Flask(__name__)

# Config
if os.getenv('DEV') == 'yes':
    app.config.from_object('remote_install.config.DevelopmentConfig')
    app.logger.info("Config: Development")
elif os.getenv('TEST') == 'yes':
    app.config.from_object('remote_install.config.TestConfig')
    app.logger.info("Config: Test")
else:
    app.config.from_object('remote_install.config.ProductionConfig')
    app.logger.info("Config: Production")

# Logging
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)

# database
db = SQLAlchemy(app)

# login
login_manager = LoginManager()
login_manager.setup_app(app)


# Business Logic
# http://flask.pocoo.org/docs/patterns/packages/
# http://flask.pocoo.org/docs/blueprints/

from remote_install.controllers.component import component
from remote_install.controllers.anamon import anamon
from remote_install.controllers.job import jobs
from remote_install.controllers.main import main

app.register_blueprint(main)
app.register_blueprint(component)
app.register_blueprint(anamon)
app.register_blueprint(jobs)

