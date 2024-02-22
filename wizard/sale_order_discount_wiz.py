from odoo import api, fields, models


class SaleOrderDiscountWizard(models.TransientModel):
    _name = 'sale.order.discount.wizard'
    _description = "Sale Order Discount Wizard"

    discount_type = fields.Selection([
        ('fix','Fix'),
        ('parentage','Parentage')],string="Discount Type",required=True)
    discount_amount = fields.Float(string="Discount Amount",required=True)

    def sale_order_discount(self):
        print("111111111111111111111111111111")
        for rec in self.sale_order_line_ids:
            print("rec:::::::::::::::::::::::",rec)
            if self.discount_type == 'fix':
                rec.price_subtotal -= self.discount_amount
            elif self.discount_type == 'parentage':
                rec.price_subtotal -= (rec.price_subtotal * self.discount_amount/100.0)








    name_id = fields.Many2one(comodel_name='sale.order', string='Name', required=True)
    sale_order_line_ids = fields.Many2many(comodel_name='sale.order.line', string='Order Lines', compute='_compute_sale_order_line_ids', store=True, domain="[('order_id', '=', name_id)]")


    @api.depends('name_id')
    def _compute_sale_order_line_ids(self):
        for wizard in self:
            lines = self.env['sale.order.line'].search([('order_id', '=', wizard.name_id.id)])
            wizard.sale_order_line_ids = [(6, 0, lines.ids)]
