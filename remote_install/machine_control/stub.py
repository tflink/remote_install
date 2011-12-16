#
# stub.py - stub used in place of actual machine control for testing and
#           development
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


import random

def get_username():
    return random.sample(['user1', 'user2', 'user3', 'user4'], 1)

def get_password():
    return random.sample(['pass1', 'pass2', 'pass3', 'pass4'], 1)

def get_url():
    return 'http://localhost:8080/guacamole'

class StubMachineControl():
    machines = []
    def create_machine(self, name, machine_template, installer, slot, kickstart):
        self.machines.append((name, installer.name, machine_template.name,
                            slot.macaddress, kickstart))
        return ["",""]

    def stop_machine(self, name):
        pass

    def delete_machine(self, name):
        pass

    def delete_disk(self, name):
        pass

    def start_machine(self, name):
        pass
