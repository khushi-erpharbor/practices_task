from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
	_inherit = 'purchase.order.line'

	discount_a = fields.Float("Discount",compute='compute_discount',store=True,readonly=False)

	@api.depends('price_unit','product_qty')
	def compute_discount(self):
		print('========',self,'========================================+++',self.discount_a)
		for rec in self:
			# discount = rec.discount_a
			po = rec.price_unit*rec.product_qty
			# print("\n\n\n\n\n\npo::::::::::::::",po)
			# discount_value = (po*discount)/100
			# print("\n\n\n\n\n\ndiscount::::::::::::",discount_value)
			# rec.price_subtotal -= discount
			# self.discount_a = discount
