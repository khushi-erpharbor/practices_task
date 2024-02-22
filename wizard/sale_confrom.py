from odoo import api, fields, models


class SaleWizardConfrom(models.TransientModel):
    _name = 'sale.confrom.wizard'


    name = fields.Char(string='Warning')
    
    def sale_order_submit_button(self):
        context = self.env.context
        if context.get('trust_not'):
            record = self.env['sale.order'].browse(context.get('active_id'))
            record.partner_id.untrustworthy = False
        if context.get('opportunity_id'):
            record = self.env['']



    @api.model
    def default_get(self, fields):
        context = self.env.context
        record = self.env['sale.order'].browse(context.get('active_id'))
        res = super(SaleWizardConfrom, self).default_get(fields)
        if self.env.context.get('trust_not'):
            res['name'] = 'Not Trust '
        if self.env.context.get('opportunity_id'):
            res['name'] = 'Opportunity NATHI'
            order.with_context({'opportunity_id': False})

        return res
