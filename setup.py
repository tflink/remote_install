from setuptools import setup, Command

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import subprocess
        errno = subprocess.call(['py.test',  'testing'])
        raise SystemExit(errno)

setup(name='remote_install',
      version='0.0.1',
      description='Application for running graphical install testing',
      author='Tim Flink',
      author_email='tflink@fedoraproject.org',
      license='GPLv3',
      url='http://localhost/something',
      packages=['remote_install', 'remote_install.controllers',
                'remote_install.machine_control', 'remote_install.view',
                'remote_install.models'],
      package_dir={'remote_install':'remote_install'},
      include_package_data=True,
      cmdclass = {'test' : PyTest},
      install_requires = [
        'pytest>=2.1.0',
        'Flask>=0.8',
        'Flask-SQLAlchemy>=0.15',
        'Flask-XML-RPC>=0.1.2',
        'Flask-Login >= 0.1',
        'SQLAlchemy >= 0.7',
        'Fabric >= 1.3.2'
     ]
     )
