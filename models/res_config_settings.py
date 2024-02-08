from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    _description = "task"
    show_history_state = fields.Selection([("draft", "Quotation State"), ("sale", "Sale Order State")],
                                          string="SHOW HISTORY", config_parameter='session_task.show_history_state')
