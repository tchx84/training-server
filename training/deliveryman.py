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

import logging

from .errors import ReadError
from .errors import SendError
from .errors import StoreError


class DeliveryMan(object):

    def __init__(self, datastore, mailman):
        self._datastore = datastore
        self._mailman = mailman

    def deliver(self):
        ''' deliver confirmations emails '''
        pendings = []

        try:
            pendings = self._datastore.pendings()
        except ReadError as error:
            logging.error(error)
            return

        for uid, email, code in pendings:
            try:
                self.request(uid, email, code)
                self._datastore.mark(code)
            except (StoreError, SendError) as error:
                logging.error(error)

    def request(self, uid, email, code):
        ''' fill body and tell mailman to send it '''
        body = self._mailman._body.format(uid, code)
        self._mailman.send(email, body)
