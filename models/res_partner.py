from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    offer_discount = fields.Boolean("Offer Discount")
    special_discount = fields.Float("Special Discount")

    def action_preview_discount(self):
        print("\n\n\n\n:::::::::::::::::::::::::::::::")
        return {
            'name': 'Discount',
            'view_mode': 'tree',
            'views': [(self.env.ref('customer_discount_tree_view').id)],
            'res_model': 'customer.discount',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
            
        }