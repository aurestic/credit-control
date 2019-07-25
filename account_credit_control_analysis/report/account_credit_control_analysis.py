# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools


class AccountCreditControlAnalysis(models.Model):
    _name = "credit.control.analysis"
    _description = "Credit Control Analysis"
    _auto = False
    _rec_name = "partner_id"

    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", readonly=True
    )
    partner_ref = fields.Char(
        related="partner_id.ref", string="Partner Ref", readonly=True
    )
    policy_id = fields.Many2one(
        comodel_name="credit.control.policy", string="Policy", readonly=True
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency", string="Currency", readonly=True
    )
    policy_level_id = fields.Many2one(
        comodel_name="credit.control.policy.level", 
        string="Overdue Level", 
        readonly=True,
    )
    level = fields.Integer(string="Level", readonly=True)
    open_balance = fields.Float(string="Open Balance", readonly=True)

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, "credit_control_analysis")
        self._cr.execute(
            """
            CREATE VIEW credit_control_analysis
            AS
            (SELECT DISTINCT ON (ccl.partner_id,
                   ccl.policy_id,
                   ccl.currency_id) ccl.id                  AS id,
                   ccl.partner_id                           AS partner_id,
                   ccl.policy_id                            AS policy_id,
                   ccl.currency_id                          AS currency_id,
                   ccl.policy_level_id                      AS policy_level_id,
                   ccpl.level                               AS level,
                (SELECT CASE 
                    WHEN ccl.currency_id IS NOT NULL THEN sum(amount_residual_currency)
                    ELSE sum(amount_residual)
                    END
                FROM account_move_line AS aml
                WHERE NOT aml.reconciled
                AND aml.id IN 
                    (SELECT move_line_id
                    FROM credit_control_line AS ccl2 
                    WHERE ccl2.partner_id=ccl.partner_id
                        AND ccl2.policy_id=ccl.policy_id
                        AND ((ccl.currency_id IS NULL AND ccl2.currency_id IS NULL) OR ccl2.currency_id=ccl.currency_id))) AS open_balance
            FROM credit_control_line AS ccl
            LEFT JOIN credit_control_policy_level AS ccpl ON ccpl.id=ccl.policy_level_id
            ORDER BY ccl.partner_id,
                    ccl.policy_id,
                    ccl.currency_id,
                    ccpl.level DESC,
                    ccl.id)
            """
        )
