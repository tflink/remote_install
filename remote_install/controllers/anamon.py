#
# anamon.py - controller for the remote logging capabilities
#
# The important parts of this were stolen pretty much verbatim out of Cobbler's
# remote.py, so extending their copyright notice.
#
# Copyright 2007-2011, Red Hat, Inc and Others
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
#   Michael DeHaan <michael.dehaan AT gmail>
#   Tim Flink <tflink@redhat.com>


from flask import Blueprint, send_from_directory
from remote_install import app
from flaskext.xmlrpc import XMLRPCHandler
import base64
import string
import os
import stat
import fcntl
import errno

handler = XMLRPCHandler('anamon')
handler.connect(app, '/anamon')

anamon = Blueprint('anamon', __name__)

@anamon.route('/aux/anamon', methods = ['GET'])
def get_anamon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                                'aux/anamon', mimetype='application/octet-stream')


@anamon.route('/aux/anamon.init', methods = ['GET'])
def get_anamon_init():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                                'aux/anamon.init', mimetype='application/octet-stream')


@handler.register
def upload_log_data(sys_name, file, size, offset, data):
    '''
    system: the name of the system
    name: the name of the file
    size: size of contents (bytes)
    data: base64 encoded file contents
    offset: the offset of the chunk
        files can be uploaded in chunks, if so the size describes
        the chunk rather than the whole file. the offset indicates where
        the chunk belongs
        the special offset -1 is used to indicate the final chunk'''
    contents = base64.decodestring(data)
    del data
    if offset != -1:
        if size is not None:
            if size != len(contents):
                return False

    #XXX - have an incoming dir and move after upload complete
    # SECURITY - ensure path remains under uploadpath
    tt = string.maketrans("/","+")
    fn = string.translate(file, tt)
    if fn.startswith('..'):
        raise Exception("invalid filename used: %s" % fn)

    # FIXME ... get the base dir from cobbler settings()
    udir = "%s/%s" % (app.config['LOG_LOCATION'], sys_name)
    if not os.path.isdir(udir):
        os.mkdir(udir, 0755)

    fn = "%s/%s" % (udir, fn)
    try:
        st = os.lstat(fn)
    except OSError, e:
        if e.errno == errno.ENOENT:
            pass
        else:
            raise
    else:
        if not stat.S_ISREG(st.st_mode):
            raise Exception("destination not a file: %s" % fn)

    fd = os.open(fn, os.O_RDWR | os.O_CREAT, 0644)
    # log_error("fd=%r" %fd)
    try:
        if offset == 0 or (offset == -1 and size == len(contents)):
            #truncate file
            fcntl.lockf(fd, fcntl.LOCK_EX|fcntl.LOCK_NB)
            try:
                os.ftruncate(fd, 0)
                # log_error("truncating fd %r to 0" %fd)
            finally:
                fcntl.lockf(fd, fcntl.LOCK_UN)
        if offset == -1:
            os.lseek(fd,0,2)
        else:
            os.lseek(fd,offset,0)
        #write contents
        fcntl.lockf(fd, fcntl.LOCK_EX|fcntl.LOCK_NB, len(contents), 0, 2)
        try:
            os.write(fd, contents)
            # log_error("wrote contents")
        finally:
            fcntl.lockf(fd, fcntl.LOCK_UN, len(contents), 0, 2)
        if offset == -1:
            if size is not None:
                #truncate file
                fcntl.lockf(fd, fcntl.LOCK_EX|fcntl.LOCK_NB)
                try:
                    os.ftruncate(fd, size)
                    # log_error("truncating fd %r to size %r" % (fd,size))
                finally:
                    fcntl.lockf(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)
    return True
