# System keyboard
keyboard us
# System language
lang en_US

# set up VNC
vnc --password={{ password }}

# Use network installation
url --url={{ tree }}

# make sure that the VNC ports are open post install
firewall --port=5901:tcp,6001:tcp

# add a test user
user --name=test --password={{ password }}

%pre
#enable installation monitoring
wget -O /tmp/anamon "http://{{ server }}:{{ port }}/aux/anamon"
python /tmp/anamon --name "test-{{ job_num }}" --server "{{ server }}" --port "{{ port }}"

# send a signal to remote_install that the init is almost ready
python -c 'import urllib2; urllib2.urlopen("http://{{ server }}:{{ port }}/job/{{ job_num }}/init_done").read()'
%end

%post
# install a vnc server
echo "installing tigervnc-server"
yum -y install tigervnc-server

# add a user 'test' and set vnc password
echo "configuring vnc"
su -l test -c 'mkdir ~/.vnc'
su -l test -c 'echo "{{ password }}" | vncpasswd -f > ~/.vnc/passwd'
su -l test -c 'chmod 600 ~/.vnc/passwd'

# set vncserver to run at boot
echo "setting vncserver to run at boot"
cat /lib/systemd/system/vncserver\@.service | sed 's/<USER>/test/g' > /lib/systemd/system/vncserver\@\:1.service
ln -sf /lib/systemd/system/vncserver\@\:1.service /etc/systemd/system/multi-user.target.wants/

# send a signal to remote_install that the installation is almost done
python -c 'import urllib2; urllib2.urlopen("http://{{ server }}:{{ port }}/job/{{ job_num }}/install_done").read()'
%end
