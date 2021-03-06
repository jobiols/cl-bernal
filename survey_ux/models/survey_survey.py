# Part of Odoo. See LICENSE file for full copyright and licensing details.

from werkzeug import urls
from odoo import api, models, fields
from odoo.exceptions import UserError


class Survey(models.Model):
    _inherit = 'survey.survey'

    code_field = fields.Char(
        compute="_compute_code_field",
        store=True
    )
    mailing_list = fields.Many2one(
        'mailing.list',
        string="Lista de Correo"
    )

    @api.depends('title')
    def name_get(self):
        res = []
        for rec in self:
            res += [(rec.id, "%s %s" % (
                                        "EN{:05}".format(rec.id),
                                        rec.title
                                        )
            )]
        return res

    def _compute_code_field(self):
        for rec in self:
            rec.code_field = "EN{:05}".format(rec.id)

    def _compute_survey_url(self):
        """ Overrides the original method in order to take into account the
            multicompany. Computes a public URL for the survey
        """
        #base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url = self.env.company.company_registry
        if not base_url:
            raise UserError('No esta definida la URL de la compañia.\nVaya a la '
                            'compañia y agregue la url en el campo "Registro de la '
                            'compañia"')
        for survey in self:
            survey.public_url = urls.url_join(base_url, "survey/start/%s" % (survey.access_token))

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    survey_name = fields.Char(
        related='survey_id.display_name',
        store=True
    )
