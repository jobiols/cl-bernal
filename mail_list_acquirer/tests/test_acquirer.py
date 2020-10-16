# Copyright 2020 jeo Sotware
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

#   Para correr los tests
#
#   Definir un subpackage tests que será inspeccionado automáticamente por
#   modulos de test los modulos de test deben enpezar con test_ y estar
#   declarados en el __init__.py, como en cualquier package.
#
#   Hay que crear una base de datos para testing como sigue:
#   - Nombre sugerido: [nombre cliente]_test
#   - Debe ser creada con Load Demostration Data chequeado
#   - Usuario admin y password admin
#   - El modulo que se quiere testear debe estar instalado.
#
#   Arrancar el test con:
#
#   oe -Q mail_list_acquirer -c bernal -d bernal_prod
#
import os, tempfile, csv
from odoo import api, models
from odoo.tests.common import SingleTransactionCase

class AcquirerTestCase(SingleTransactionCase):

    def test_get_file_data(self):

        import wdb;wdb.set_trace()

        tf = tempfile.NamedTemporaryFile()
        with open(tf, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter='|')

            writer.writerow(
                ['30698426612',
                'lista campaña 1',
                'gervasio@perinola.com',
                'Gervasio Atorra'])

        aq = self.env['mail.list.acquirer']

        aq.get_file_data(filename, False)
