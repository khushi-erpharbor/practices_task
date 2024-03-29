from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    offer_discount = fields.Boolean("Offer Discount")
    untrustworthy = fields.Boolean("Untrustworthy")
    special_discount = fields.Float("Special Discount")
    portal_partner = fields.Boolean("Portal Partner")
    saw_partner = fields.Boolean("Saw Partner")
    

    def action_preview_discount(self):
        print("\n\n\n\n:::::::::::::::::::::::::::::::")
        return {
            'name': 'Discount',
            'view_mode': ',formtree',
            # 'views': [(self.env.ref('practice.customer_discount_tree_view').id)],
            'res_model': 'customer.discount',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('partner_id','=',self.id)]
            
        }
   



    #   def action_preview_untrustworthy(self):
        # return {
        #     'name': 'Discount',
        #     'view_mode': 'tree',
        #     'views': [(self.env.ref('customer_discount_tree_view').id)],
        #     'res_model': 'customer.discount',
        #     'type': 'ir.actions.act_window',
        #     'target': 'current',
        #     'domain': domain,
            
        # }