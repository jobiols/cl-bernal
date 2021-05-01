from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime,  timedelta
import logging
_logger = logging.getLogger(__name__)


class Survey(models.Model):
    _inherit = 'survey.survey'

    @api.model
    def send_survey(self):
        """ Sobreescribimos este metodo para tener en cuenta la lista de correo agregada
        """
        for survey in self:
            # obtenemos los emails de la lista de correos
            emails = survey.mailing_list.contact_ids.mapped('email')

            # aqui agregemos los mails de la lista al campo survey.emails
            if not survey.emails:
                survey.emails = ','.join(emails)
            else:
                # quitar espacios en blanco si existen
                survey.emails = survey.emails.strip()
                # quitar ultima coma si existe
                survey.emails = survey.emails.strip(',')
                # agregar una coma
                survey.emails += ','
                # agregar los mails de la lista
                survey.emails += ','.join(emails)

            local_context = {
                'default_public': survey.access_mode,
                'default_emails': survey.emails,
                'default_partner_ids': survey.partner_ids,
            }
            fields_get = self.env['survey.invite'].fields_get()
            composed_survey = survey.with_context(local_context).action_send_survey()
            vals = self.env['survey.invite'].with_context(
                composed_survey.get('context')).default_get(fields_get)
            wizard = self.env['survey.invite'].create(vals)
            wizard.action_invite()
        return True
