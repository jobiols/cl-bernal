import csv
import os
from datetime import datetime
from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class MailListAcqirer(models.AbstractModel):
    _name = "mail.list.acquirer"
    _description = "Mailing Acquirer"

    @staticmethod
    def new_file(path):
        """ Devuelve True si hay un archivo nuevo para leer
        """
        try:
            files = os.listdir(path)
        except FileNotFoundError:
            _logger.error("The path %s is not found. See 'batch.upload.path "
                          "parameter'", path)
            return False
        return files

    @staticmethod
    def get_file(path):
        """ Devuelve el nombre del archivo nuevo
        """
        files = os.listdir(path)
        return '%s/%s' % (path, files[0]) if files else False

    @staticmethod
    def bkp_filename(path):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        return '%s/mails_%s.csv' % (path, timestamp)

    def get_file_data(self, filename, path_bkp):
        """ Leer el archivo y devolver una estructura con los datos
            una vez leido lo borramos
        """
        CUIT = 0
        LIST = 1
        EMAIL = 2
        NAME = 3
        ret = dict()

        def process_file_line(row):
            """ row: List of parameters
                [cuit, maillist, email, name]

                return: dict
                ret = {
                  'id_lista_454': [ {'cuit': 213456,
                                     'name': 'juan',
                                     'email': 'juan@gmail.com'},
                                    {'cuit': 213456,
                                     'name': 'juan',
                                     'email': 'juan@gmail.com'},
                                   ],
                  'id_lista_32':  [ {'cuit': 213456,
                                     'name': 'juan',
                                     'email': 'juan@gmail.com'},
                                    {'cuit': 213456,
                                     'name': 'juan',
                                     'email': 'juan@gmail.com'},
                                   ]
                },
            """

            pack = {
                'cuit': row[CUIT],
                'email': row[EMAIL],
                'name': row[NAME]
            }
            if row[LIST] in ret:
                maillist = ret[row[LIST]]
                maillist.append(pack)
            else:
                ret[row[LIST]] = [pack]

        try:
            _f = open(filename)
        except OSError:
            _logger.error("Can not read file %s", filename)
            return False

        with _f:
            reader = csv.reader(_f, delimiter='|')
            for row in reader:
                process_file_line(row)

        if path_bkp:
            try:
                os.rename(filename, self.bkp_filename(path_bkp))
            except OSError as ex:
                _logger.error("Can not move file %s - %s", filename, str(ex))

        return ret

    def save_mails(self, data):
        """ Salvar los mails en las listas de correo
        """
        mailing_list_obj = self.env['mailing.list']
        contact_obj = self.env['mailing.contact']
        mailing_subscription_obj = self.env['mailing.contact.subscription']

        for list_name in data:

            # busco el nombre en el modelo
            list_id = mailing_list_obj.search([('name', '=', list_name)])
            if not list_id:
                list_id = mailing_list_obj.create({'name': list_name})

            # obtengo los datos que van en la lista
            packs = data[list_name]
            for contact in packs:
                domain = [('email', '=', contact['email'])]
                contact_id = contact_obj.search(domain)
                if contact_id:
                    contact_id.name = contact['name']
                else:
                    contact_id = contact_obj.create({'name':contact['name'],
                                                     'email':contact['email']})

                # obtengo la subscripcion
                domain = [('contact_id', '=', contact_id.id),
                          ('list_id', '=', list_id.id)]
                mailing_subscription_id = mailing_subscription_obj.search(domain)
                if not mailing_subscription_id:
                    mailing_subscription_obj.create({
                        'contact_id': contact_id.id,
                        'list_id': list_id.id,
                    })

                # veo si el contacto no esta en la lista, y lo agrego
                if mailing_subscription_id not in contact_id.subscription_list_ids:
                    contact_id.subscription_list_ids += mailing_subscription_id

    def read_mail_files(self):
        """ Lanzado por cron para levantar los archivos de mails
        """
        config = self.env['ir.config_parameter'].sudo()
        path = config.get_param("batch.upload.path", '/var/log/odoo/upload').rstrip('/')
        path_bkp = config.get_param("batch.upload.path.bkp", '/var/log/odoo/bkp').rstrip('/')

        while self.new_file(path):
            filename = self.get_file(path)
            data = self.get_file_data(filename, path_bkp)
            self.save_mails(data)
