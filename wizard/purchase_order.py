from odoo import api, fields, models


class WizardPractical(models.TransientModel):
	_name = 'create.purchase.order'
	_description = 'Create Purchase order in wizard'

	vendor = fields.Many2one("res.partner",string="Vendor")
	company = fields.Many2one('res.company',string="Company")

	def create_purchase_order(self):
		print("\n\nWizard\n\n")
		for rec in self:
			product_ids = self.env.context.get('active_id')
			record = self.env['purchase.order'].create({
				'partner_id':rec.vendor.id,
				'company_id':rec.company.id,
				'order_line':[(
					0, 0,{
						'order_id':rec.id,
						'product_id':product_ids,
					})]
				})
			return record
			


