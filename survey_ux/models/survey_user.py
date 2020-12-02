# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools, models, fields, api

class SurveyUserConsolidatedLine(models.Model):
    """ Este modelo muestra las respuestas a las encuestas de tipo "simple_choice"
    """
    _name = 'survey_ux.consolidated.line'
    _description = "consolidated answers for survey"
    _auto = False

    question = fields.Char(
    )
    question_id = fields.Many2one(
        'survey.question'
    )
    answer = fields.Char(
    )
    participation = fields.Integer(
    )
    participationx100 = fields.Float(
        compute="_compute_participationx100"
    )

    def _compute_participationx100(self):
        for rec in self:
            count = len(rec.question_id.user_input_line_ids)
            rec.participationx100 = rec.participation / count * 100

    def init(self):
        """ Create the view """
        tools.drop_view_if_exists(self._cr, self._table)
        query = """
            SELECT
                sq.id+sl.id as id,
                sq.title as question,
                sq.id as question_id,
                sl.value as answer,
                count(sl.value) as participation
            FROM survey_question sq
            JOIN survey_user_input_line suil
            ON sq.id = suil.question_id
            JOIN survey_label sl
            ON sl.id = suil.value_suggested
        where sq.question_type = 'simple_choice'
        group by sl.value, sq.title, sq.id, sl.id
        order by sq.title
        """
        sql = 'CREATE OR REPLACE VIEW %s as (%s)'
        self._cr.execute(sql % (self._table, query))
