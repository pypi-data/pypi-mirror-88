#!/usr/bin/python3
# -*- coding: utf-8

#  nmap-scan
#
#  Nmap wrapper for python
#
#  Copyright (c) 2020 Fabian Fröhlich <mail@nmap-scan.de> <https://nmap-scan.de>
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  For all license terms see README.md and LICENSE Files in root directory of this Project.
#
#  Checkout this project on github <https://github.com/f-froehlich/nmap-scan>
#  and also my other projects <https://github.com/f-froehlich>


import logging

from nmap_scan.Scripts.SSLEnumCiphers import SSLEnumCiphers
from nmap_scan.Scripts.UnknownScript import UnknownScript


def parse(script_xml):
    script_id = script_xml.attrib['id']
    logging.info('Parsing script with id "{id}"'.format(id=script_id))

    if 'ssl-enum-ciphers' == script_id:
        return SSLEnumCiphers(script_xml)

    logging.debug(
        'No specific script class for script with id "{id}" exists. Using UnknownScript.'.format(id=script_id))
    return UnknownScript(script_xml)
