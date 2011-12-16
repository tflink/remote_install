#!/usr/bin/env python

import remote_install

if __name__ == '__main__':
    if remote_install.app.debug:
        remote_install.app.run(debug=True)
    else:
        remote_install.app.run(host='0.0.0.0')

