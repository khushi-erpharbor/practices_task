from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CustomerDiscount(models.Model):
    _name = "customer.discount"
    _description = "task"

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Partner Id")
    amount = fields.Float(
        string='Amount')

    # _sql_constraints = [
    #     ('uniq_partner_id', 'unique (partner_id)', 'This customer is already existed.'),
    # ]

    @api.constrains('partner_id')
    def _check_names(self):
        for rec in self:
            recorde = self.search([("partner_id.name", "=", rec.partner_id.name), ('id','!=',self.id)])
            if recorde:
                raise ValidationError('%s Already Exists In Name List.' % rec.partner_id.name)