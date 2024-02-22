from odoo import models, fields, api


class PurchaseTemplate(models.Model):
    _inherit = 'product.template'

    is_no_any_discount = fields.Boolean(string='No Any Discount')