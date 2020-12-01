# Part of Odoo. See LICENSE file for full copyright and licensing details.

from werkzeug import urls
from odoo import api, models, fields
from odoo.exceptions import UserError


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input_line'

    participacion = fields.Integer(
    )
    participacionx100 = fields.Float(
    )

    def compute_participacion(self):
        """ Calcula las variables participacion y participacionx100
        """
        domain = [('question_type', '=', 'simple_choice')]
        domain += [('user_input_line_ids', '!=', False)]

        # cada una de las preguntas de tipo simple_choice con respuestas
        questions_ids = self.env['survey.question'].search(domain)

        for question_id in questions_ids:
            line_ids = question_id.user_input_line_ids

            # cantidad total de input lines en esta respuesta
            count = len(line_ids)

            # el conjunto de etiquetas que tienen las input lines
            labels = line_ids.mapped(lambda x: x.value_suggested)

            # verificar cuantas veces aparece cada label
            for label in labels:
                # por cada label obtener el recorset de respuestas que lo contiene
                tmp = line_ids.search([('value_suggested', '=', label.id)])
                qty = len(tmp)
                # salvar las participaciones a todos los records con una sola asignacion
                # ... esto anda solo a partir de la v13 ...
                tmp.participacion = qty
                tmp.participacionx100 = qty/count * 100
