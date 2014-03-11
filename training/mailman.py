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

import smtplib
import logging

from email.mime.text import MIMEText

from .errors import SendError


class MailMan(object):

    def __init__(self, host, port, user, password, mime, subject, body):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._mime = mime
        self._subject = subject
        self._body = body

    def send(self, email, body):
        message = MIMEText(body, self._mime)
        message['Subject'] = self._subject

        try:
            server = smtplib.SMTP(self._host, self._port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self._user, self._password)
            server.sendmail(self._user, [email], message.as_string())
            server.quit()
        except Exception as error:
            logging.error(error)
            raise SendError(error)
