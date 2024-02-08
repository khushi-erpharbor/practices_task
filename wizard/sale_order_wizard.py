from odoo import api, fields, models


class SaleOrderWizad(models.TransientModel):
    _name = 'sale.order.wizard'

    name = fields.Many2one('res.partner', string="Customer", readonly=True)
    product = fields.Many2one('product.template', string="Product", readonly=True)
    order_line_ids = fields.Many2many(
        comodel_name='sale.order.line'
    )
    show_history = fields.Selection([("draft", "Quotation State"), ("sale", "Sale Order State")],
                                    string="SHOW HISTORY", config_parameter='session_task.show_history')

    @api.model
    def default_get(self, fields_list):
        context_sale_order_line_id = self.env.context.get("active_id")

        record = self.env["sale.order.line"].browse(context_sale_order_line_id)
        res = super().default_get(fields_list)
        res["name"] = record.order_id.partner_id
        res["product"] = record.product_template_id
        show_history = self.env['ir.config_parameter'].get_param('session_task.show_history_state')
        print(show_history)
        store_record = self.env["sale.order.line"].search([('order_id.partner_id.name', '=', res["name"].name),
                                                           ('product_template_id.name', '=', res["product"].name),
                                                           ('order_id.state', '=', show_history)])
        res.update({
            'order_line_ids': [(fields.Command.set([int(record) for record in store_record]))]
        })
        return res
