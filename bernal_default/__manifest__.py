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
#   le agregamos esto
##############################################################################

{
    'name': 'bernal',
    'version': '13.0.0.0.0',
    'category': 'Tools',
    'summary': "Customizacion Sanatorio Bernal",
    'author': "jeo Software",
    'website': 'http://github.com/jobiols/cl-bernal',
    'license': 'AGPL-3',
    'depends': [ ],
    'installable': True,

    # manifest version, if omitted it is backward compatible
    'env-ver': '2',

    # if Enterprise it installs in a different directory than community
    'odoo-license': 'CE',

    'port': '8069',

    'git-repos': [
        'git@github.com:jobiols/cl-bernal.git',
        'https://github.com/jobiols/odoo-addons.git',
        'git@github.com:jobiols/odoo-jeo-ce.git',
        #'git@github.com:jobiols/odoo-private-addons.git',
        'https://github.com/marionumza/rep-sb.git',

        # para localizacion argentina
        'https://github.com/ingadhoc/odoo-argentina.git',
        'https://github.com/ingadhoc/odoo-argentina-ce.git',
        'https://github.com/ingadhoc/aeroo_reports.git',
        'https://github.com/ingadhoc/account-payment.git',
        'https://github.com/ingadhoc/account-financial-tools.git',
    ],

    # list of images to use in the form 'name image-url'
    'docker-images': [
        'odoo jobiols/odoo-jeo:13.0',
        'postgres postgres:10.1-alpine',
        'nginx nginx',
    ]
}
