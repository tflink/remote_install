activate_this = '/var/www/remote_graphical/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from remote_graphical import app as application
