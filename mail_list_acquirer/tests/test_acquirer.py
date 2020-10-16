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
#   oe -Q mail_list_acquirer -c bernal -d bernal_test
#
import os, tempfile, csv
from odoo import api, models
from odoo.tests.common import SingleTransactionCase

class AcquirerTestCase(SingleTransactionCase):

    def test_get_file_data(self):
        tf = tempfile.NamedTemporaryFile()
        with open(tf.name, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter='|')

            writer.writerow(['3069','lista_1','gervasio@per.com','Gervasio'])
            writer.writerow(['3069','lista_2','juan@per.com','Juan'])
            writer.writerow(['3069','lista_2','pepito@per.com','Pepito'])
            writer.writerow(['3069','lista_2','juanito@per.com','Juanito'])
            writer.writerow(['3069','lista_1','cacho@per.com','Cacho'])

        aq = self.env['mail.list.acquirer']
        data = aq.get_file_data(tf.name, False)

        lista_1 = [{'cuit': '3069', 'email': 'gervasio@per.com', 'name': 'Gervasio'},
                   {'cuit': '3069', 'email': 'cacho@per.com', 'name': 'Cacho'}]

        self.assertEqual(data['lista_1'], lista_1)
        lista_2 = [{'cuit': '3069', 'email': 'juan@per.com', 'name': 'Juan'},
                   {'cuit': '3069', 'email': 'pepito@per.com', 'name': 'Pepito'},
                   {'cuit': '3069', 'email': 'juanito@per.com', 'name': 'Juanito'}]
        self.assertEqual(data['lista_2'], lista_2)
