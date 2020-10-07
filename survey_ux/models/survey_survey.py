# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class Survey(models.Model):
    _inherit = 'survey.survey'

    code_field = fields.Char(
        compute="_compute_code_field",
    )

    @api.depends('title')
    def name_get(self):
        res = []
        for rec in self:
            res += [(rec.id, "%s %s" % (rec.code_field, rec.title))]
        return res

    def _compute_code_field(self):
        for rec in self:
            rec.code_field = "EN{:05}".format(rec.id)