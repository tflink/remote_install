#
# machine_control - basic, primitive script using fabric to execute commands
#                   on a remote host to create and manage virtual machines
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


from remote_install import app
from fabric.api import run, settings, env
import re

class FabricController():
    hostlist = [app.config['VIRT_HOST']]
    env.key_filename = [app.config['SSH_KEY']]

    disk_prefix = 'remote_'
    vg_name = app.config['VIRT_VG_NAME']

    def make_install_cmd(self, name, disk, memory, location, macaddress,
                            kickstart, vncport):
        return "virt-install --name=%s --hvm --graphics vnc,password=password,port=%d" \
                " --video=cirrus --arch=x86_64 --vcpus=1 --ram=%d" \
                " --os-type=linux --os-variant=fedora15" \
                " --disk path=/dev/%s/%s,device=disk,bus=virtio" \
                " --location='%s' --network network=default,mac='%s'" \
                " --extra-args='ks=%s'" \
                % (name, vncport, memory, self.vg_name, disk, location, macaddress, kickstart)

    def list_disk(self):
        for host in self.hostlist:
            with settings(host_string = host):
                return run('lvdisplay | grep \'LV Name\'')

    def create_disk(self, size, name):
        with settings(host_string = self.hostlist[0]):
            output = run('lvcreate -n %s -L %dG %s' %
                    (name, size, self.vg_name))
            return re.search('"(.+)"', output).group(1)

    def delete_disk(self, name):
        with settings(host_string = self.hostlist[0]):
            run('lvchange -an /dev/%s/%s%s' % (self.vg_name, self.disk_prefix, name))
            run('lvremove -f /dev/%s/%s%s' % (self.vg_name, self.disk_prefix, name))

    def create_vm(self, name, disk, memory, location, macaddress, kickstart, vncport):
        cmd = self.make_install_cmd(name, disk, memory, location, macaddress,
                                    kickstart, vncport)
        with settings(host_string = self.hostlist[0]):
            run(cmd)

    def create_machine(self, name, machine_template, installer, slot, kickstart):
        disk_size = machine_template.disk
        memory = machine_template.memory
        location = installer.location
        macaddress = slot.macaddress
        vncport = int('590%d' % slot.id )

        diskname = '%s%s' % (self.disk_prefix, name)
        disk_log = self.create_disk(disk_size, diskname)
        vm_log = self.create_vm(name, diskname, memory, location, macaddress, kickstart, vncport)

        return [disk_log, vm_log]

    def stop_machine(self, name):
        with settings(host_string = self.hostlist[0]):
            run('virsh destroy %s' % name)

    def delete_machine(self, name):
        with settings(host_string = self.hostlist[0]):
            run('virsh undefine  %s' % name)

    def start_machine(self, name):
        with settings(host_string = self.hostlist[0]):
            run('virsh start  %s' % name)


