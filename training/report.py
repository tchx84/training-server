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


class Report(object):

    @staticmethod
    def parse(data):
        ''' convert from transport format to SQL format '''
        trainees = []
        tasks = []
        confirmations = []

        # XXX find a proper library to do this convertions
        for entry in data:
            trainees.append(entry[0])
            tasks += map(lambda e: entry[0][:2] + e, entry[1])
            confirmations += [entry[0][:2]]

        return trainees, tasks, confirmations
