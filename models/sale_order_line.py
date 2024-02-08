from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "task"

    quantity = fields.Float("Quantity",compute="all_quantity")
    display_image = fields.Boolean("Display Image")
    purchase_id = fields.Many2one('purchase.order',string="Purchase")

    @api.depends('order_line.product_uom_qty')
    def all_quantity(self):
        for rec in self.order_line:
            self.quantity += rec.product_uom_qty

    @api.onchange('purchase_id')
    def onchange_value(self):
        self.update({
            'order_line': [(fields.Command.clear())]
        })
        value = self.purchase_id.order_line
        for line in value:
            self.update({
                'order_line': [(fields.Command.create({'product_template_id':line.product_id}))]
            })
            
    # @api.onchange('purchase_id')
    # def onchange_purches(self):
    #     if self.purchase_id:
    #         print("----------",self.purchase_id)
    #         self.order_line = [(5, 0, 0)]
    #         for line in self.purchase_id.order_line:
    #             vals = {
    #                 'product_id': line.product_id.id,
    #                 'product_uom_qty': line.product_qty,
    #             }
    #             self.order_line += self.order_line.new(vals)


    def sale_order_button(self):
        print("\n\n\n::::::::::::::::;")
        delete = self.order_line[2:]
        print("\n\n\n\ndelte:::::::::::;",delete)
        delete.unlink() 
