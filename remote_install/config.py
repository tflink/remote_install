#!/usr/bin/env python

# http://flask.pocoo.org/docs/config/#development-production

class Config(object):
    SECRET_KEY = 'qp*mhouie48a6-=dn72wu6h)y5f)@5-nqvht%xo4h)9e8i8p=d'
    SITE_NAME = 'localhost'
    SYS_ADMINS = ['foo@localhost']
    LOG_LOCATION = '/tmp/anamon'
    LOG_PREFIX = 'http://localhost/anamon'
    SSH_KEY = '/tmp/test_rsa'
    VIRT_HOST = 'root@localhost'
    VIRT_VG_NAME = 'vg_test'
    KICKSTART_SERVER = 'localhost'
    KICKSTART_PORT = 5000

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/remote.db'
    FAKE_MACHINE = False

class TestConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    FAKE_MACHINE = True


class DevelopmentConfig(Config):
    '''Use "if app.debug" anywhere in your code, that code will run in development code.'''
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/remote.db'
    FAKE_MACHINE = True

