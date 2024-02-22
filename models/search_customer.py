from odoo import models, fields, api


class SearchCustomer(models.Model):
    _name = 'search.customer'
    _description = 'Search Customer'
    _rec_name = 'customer_id'

    customer_id = fields.Many2one(comodel_name='res.partner',string="Customer")
    mobile = fields.Char("Mobile")
    phone = fields.Char("Phone")

    @api.onchange('customer_id')
    def onchange_customer(self):
        self.mobile = self.customer_id.mobile,
        self.phone = self.customer_id.phone


    def search_customer(self):
        print("Search")
        action_window = {
            'name': 'Search Customer',
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'res_id': self.customer_id.id,
        }
        return action_window


    def print_customer(self):
        print("Print")
        # return self.env.ref('practice.action_customer_record').report_action(self.customer_id)