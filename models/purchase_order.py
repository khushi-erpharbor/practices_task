from odoo import models, fields, api


class Purchase(models.Model):
    _inherit = 'purchase.order'

    image = fields.Boolean("Image ?")
    sale_order_id = fields.Many2one("sale.order",string="Sale Order Id")
    # purchase_unique = fields.Char("purchase_unique")

    def send_by_email(self):
        print("SEND BY EMAIL")
        template_id = self.env.ref('practice.purchase_order_email')
        attch = self.env['ir.attachment'].search([
            ('res_model','=','purchase.order'),
            ('res_id','=',self.id)])
        template_id.send_mail(self.id,force_send=True,email_values={'attachment_ids': [(6, 0, attch.ids)]})
        return True


class PurchaseOrderLine(models.Model):
	_inherit = 'purchase.order.line'

	product_image = fields.Binary("Product Image",related='product_id.image_1920')

    # @api.onchange('product_id')
    # def onchange_image(self):
    #     print("\n\n\nself::::::::::",self)
    #     self.product_image = self.product_id.image_1920

