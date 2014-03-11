#!/usr/bin/env python

# Copyright (c) 2014 Martin Abente Lahaye. - tch@sugarlabs.org
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
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import os

from ConfigParser import ConfigParser

from training.datastore import DataStore
from training.deliveryman import DeliveryMan
from training.mailman import MailMan


def main():
    script_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_path, 'etc/training.cfg')
    subject_path = os.path.join(script_path, 'data/subject.text')
    body_path = os.path.join(script_path, 'data/body.text')

    config = ConfigParser()
    config.read(config_path)

    with open(subject_path) as file:
        subject = file.read()

    with open(body_path) as file:
        body = file.read()

    mailman = MailMan(config.get('smtp', 'host'),
                      config.get('smtp', 'port'),
                      config.get('smtp', 'username'),
                      config.get('smtp', 'password'),
                      config.get('smtp', 'mime'),
                      subject, body)

    datastore = DataStore(config.get('database', 'host'),
                          config.getint('database', 'port'),
                          config.get('database', 'username'),
                          config.get('database', 'password'),
                          config.get('database', 'database'))

    deliveryman = DeliveryMan(datastore, mailman)
    deliveryman.deliver()

if __name__ == '__main__':
    main()
