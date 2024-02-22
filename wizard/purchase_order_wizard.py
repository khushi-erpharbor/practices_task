from odoo import api, fields, models


class PurchaseWizard(models.TransientModel):
    _name = 'purchase.wizard'

    product_ids = fields.Many2many('product.product', string="Product")
    name = fields.Char(string='name')

    def action_add_product(self):
        if self._context.get('active_model') == 'purchase.order':
            ctx = self.env.context
            po = self.env['purchase.order'].browse(ctx.get('active_id'))
            line_ids = []
            for record in self.product_ids:
                line_id = self.env['purchase.order.line'].create({
                        'product_id': record.id,  
                        'order_id': po.id
                        }).id
                line_ids.append(line_id)

            return {
                'name': 'Add Lines',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'purchase.order.line',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('id','in',line_ids)],
                # 'context':{
                #     'active_model':self.env.context.get('active_model'),
                # },
            }

        elif self._context.get('active_model') == 'sale.order':
            ctx = self.env.context
            so = self.env['sale.order'].browse(ctx.get('active_id'))
            line = []
            for record in self.product_ids:
                line_id = self.env['sale.order.line'].create({
                        'product_id': record.id,  
                        'order_id': so.id
                        }).id
                print("line_id:::::::::::::::",line_id)
                line.append(line_id)

            return {
                'name': 'Add Lines',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order.line',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('id','in',line)]
            }

    # def action_add_product(self):
    #     ctx = self.env.context
    #     po = self.env['purchase.order'].browse(ctx.get('active_id'))
    #     print(po)



        



    def default_get(self,vals):
        print(self.env.context,'======================')
        print(vals,'+++++++++++++++++++++',self)
        res = super().default_get(vals)
        print("\n\n\n\nres::::::::::::::::::::::::",res)
        res["name"] = "hello"
        return res

