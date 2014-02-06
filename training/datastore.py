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

import MySQLdb
import logging

from .errors import StoreError
from .errors import ReadError
from .report import Report


class DataStore(object):

    QUERY_TRAINEES = 'INSERT INTO trainees '\
                     '(uid, email, name, school, '\
                     'percentage, version, reported) '\
                     'values (%s, %s, %s, %s, %s, %s, '\
                     'UNIX_TIMESTAMP(now())) '\
                     'ON DUPLICATE KEY UPDATE '\
                     'name = VALUES(name), '\
                     'school = VALUES(school), '\
                     'percentage = VALUES(percentage), '\
                     'version = VALUES(version), '\
                     'reported = VALUES(reported)'

    QUERY_TASKS = 'INSERT INTO tasks '\
                  '(trainee_uid, trainee_email, '\
                  'task, start, end, accumulated) '\
                  'values (%s, %s, %s, %s, %s, %s) '\
                  'ON DUPLICATE KEY UPDATE '\
                  'trainee_uid = VALUES(trainee_uid)'

    QUERY_CONFIRMATIONS = 'INSERT INTO confirmations '\
                          '(trainee_uid, trainee_email, '\
                          'code, requested, confirmed) '\
                          'values (%s, %s, UUID(), FALSE, FALSE) '\
                          'ON DUPLICATE KEY UPDATE '\
                          'trainee_uid = VALUES(trainee_uid)'

    QUERY_CONFIRM = 'UPDATE confirmations SET confirmed = TRUE '\
                    'WHERE code = %s'

    QUERY_REQUEST = 'SELECT trainee_uid, trainee_email, code '\
                    'FROM confirmations '\
                    'WHERE requested = FALSE'

    QUERY_REQUESTED = 'UPDATE confirmations '\
                      'SET requested = TRUE '\
                      'WHERE code = %s'

    def __init__(self, host, port, username, password, database):
        self._connection = MySQLdb.connect(host=host,
                                           port=port,
                                           user=username,
                                           passwd=password,
                                           db=database)

    def store(self, data):
        trainees, tasks, confirmations = Report.parse(data)
        self._execute_write([(self.QUERY_TRAINEES, trainees),
                             (self.QUERY_TASKS, tasks),
                             (self.QUERY_CONFIRMATIONS, confirmations)])

    def confirm(self, code):
        ''' mark this confirmation code as confirmed '''
        self._execute_write([(self.QUERY_CONFIRM, [[code]])])

    def pendings(self):
        ''' return list of pending requests to be send '''
        return self._execute_read(self.QUERY_REQUEST)

    def mark(self, code):
        ''' mark this confirmation code as requested '''
        self._execute_write([(self.QUERY_REQUESTED, [[code]])])

    def _execute_read(self, query):
        self._connection.ping(True)
        try:
            cursor = self._connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as error:
            logging.error(error)
            raise ReadError(error)
        finally:
            cursor.close()

    def _execute_write(self, queries):
        self._connection.ping(True)
        try:
            self._connection.begin()
            cursor = self._connection.cursor()
            for query, params in queries:
                cursor.executemany(query, params)
            self._connection.commit()
        except Exception as error:
            print error
            self._connection.rollback()
            raise StoreError(error)
        finally:
            cursor.close()

    def __del__(self):
        if hasattr(self, '_connection') and self._connection is not None:
            self._connection.close()
