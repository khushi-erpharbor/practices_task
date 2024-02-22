from odoo import models, fields, api,_
from odoo.exceptions import ValidationError



class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "task"
    purchase_view = 0

    quantity = fields.Float("Quantity",compute="compute_quantity")
    display_image = fields.Boolean("Display Image")
    purchase_id = fields.Many2one('purchase.order',string="Purchase")
    purchase_state =fields.Boolean("purchase_state")
    purchase_count = fields.Integer(string="Purchase Count",compute='compute_purchase_id')
    total_discount = fields.Float(string='Total Discount', store=True)
    submit = fields.Boolean("Submit")
    users = fields.Many2many('res.users',string='users',required=True,groups="practice.approval_group_view")
    name = fields.Char(
        string="Order Reference",
        required=True, copy=False, readonly=True,
        index=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: _('Odoo'))
    quotation = fields.Text(string='Quotation')
    sale_order = fields.Text(string='Sale Order')

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _("Odoo")) == _("Odoo"):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('sale.order.sl')
        return super(SaleOrder,self).create(vals_list)

    def write(self,vals):
        if vals.get('state') == 'draft':
            if not self.quotation:
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.qu')
                self.quotation = vals['name']
            else:
                vals['name'] = self.quotation

        if vals.get('state') == 'sale':
            if not self.sale_order:
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.sl')
                self.sale_order = vals['name']
            else:
                vals['name'] = self.sale_order

        return super().write(vals)

        #     vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.qu')
        #     self.quotation = vals['name']
        # else:
        #     vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.sl')
        #     self.quotation = vals['name']
        # return super().write(vals)




    def purchase_order_wizard_action_one(self):
        return{'type': 'ir.actions.act_window',
            'name': ("Cash Basis Entries"),
            'res_model': 'purchase.wizard',
            'view_mode': 'form',
            'views': 'from',
            'context':{'v':1}
        }

    @api.onchange('order_line')
    def check_product_discount(self):
        special_discount = self.partner_id.special_discount
        for rec in self.order_line:
            rec.discount_amount = 0.0
            is_boolean = rec.product_id.is_no_any_discount
            print("boolean:::::::::::::::::::::::",is_boolean)
            if is_boolean:
                rec.discount = 0.0
                rec.discount_amount = 0.0
            else:
                rec.discount = special_discount
                price_subtotal = rec.price_unit * rec.product_uom_qty
                discount_value = (price_subtotal *rec.discount )/100
                rec.price_subtotal -= discount_value
                rec.discount_amount = discount_value
        self.total_discount = sum(rec.discount_amount for rec in self.order_line)
    
    """
    harsh sir server action context task.
    """
    def write(self,values):
        print("\n\n\n\n\nvalues------------------------------------",values)
        print("\n\n\n\n\n------------------------------",self._context)
        if values.get('origin') == False and self._context.get('k'):
            values.pop('origin')
        return super(SaleOrder,self).write(values)

    @api.onchange('discount')
    def _onchange_account_type(self):
        print("\n\n\n\nha te true che",self)
        # if self.group_discount_per_so_line == True:
            # self.tax_ids = False
            

    @api.depends('order_line.product_uom_qty')
    def compute_quantity(self):
        self.quantity = 0
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
        delete = self.order_line[2:]
        delete.unlink()


    # @api.depends('purchase_id')
    def compute_purchase_id(self):
        for order in self:
            order.purchase_count = self.env['purchase.order'].search_count([('sale_order_id','=',self.id)])


    def purchase_create(self):
        self.purchase_state = True
        purchase_order = self.env['purchase.order'].create({
            'partner_id':self.partner_id.id,
            'date_order':fields.Date.today(),
            'sale_order_id':self.id,
            })

        for line in self.order_line:
            purchase_order_line = self.env['purchase.order.line'].create({
                'product_id':line.product_id.id,
                'product_qty': line.product_uom_qty,
                'name': line.name,
                'price_unit': line.price_unit,
                'price_subtotal': line.price_subtotal,
                'order_id':purchase_order.id
                })
            
        # action = {
        #     'name':'Purchase Order',
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'purchase.order',
        #     'view_mode': 'form',
        #     'res_id': purchase_order.id,
        #     'target': 'current', 
        # }
        # return action

    def purchase_order_line(self):
        print(":::::;;;")
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order Lines',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain':[('sale_order_id','=',self.id)],
        }
        return action

    def action_send_mail(self):
        template_id = self.env.ref('practice.salary_attechment_email_invite')
        attch = self.env['ir.attachment'].search([
            ('res_model', '=', 'sale.order'), 
            ('res_id', '=', self.id)])
        template_id.send_mail(self.id,force_send=True,email_values={'attachment_ids': [(6, 0, attch.ids)]})
        return True
    

class Purchase(models.Model):
    _inherit = 'purchase.order'

    image = fields.Boolean("Image ?")
    sale_order_id = fields.Many2one("sale.order",string="Sale Order Id")
    # purchase_unique = fields.Char("purchase_unique")


class PurchaseLine(models.Model):
    _inherit = 'purchase.order.line'

    product_image = fields.Binary("Product Image",related='product_id.image_1920')

    # @api.onchange('product_id')
    # def onchange_image(self):
    #     print("\n\n\nself::::::::::",self)
    #     self.product_image = self.product_id.image_1920


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount_amount = fields.Float("Discount Value")

    