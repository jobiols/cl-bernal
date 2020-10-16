##############################################################################
#
#    Copyright (C) 2020  jeo Software  (http://www.jeosoft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your optiogitn) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################

{
    'name': 'Mail list Acquirer',
    'version': '13.0.1.0.0',
    'category': 'Tools',
    "development_status": "Alpha",  # "Alpha|Beta|Production/Stable|Mature"
    'summary': "Genera lista de correo a partir de archivos de texto",
    'author': "jeo Software",
    'website': 'http://github.com/jobiols/cl-bernal',
    'license': 'AGPL-3',
    'depends': [
        'mass_mailing'
        ],
    'data': [
        'data/cron_data.xml'
        ],
    'installable': True,
    'sequence': 2
}
