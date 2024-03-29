from odoo import models, fields, api,_
from odoo.exceptions import ValidationError



class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "task"
    # _inherit = ['mail.thread','mail.activity.mixin']
    purchase_view = 0

    quantity = fields.Float("Quantity",compute="compute_quantity")
    display_image = fields.Boolean("Display Image")
    purchase_id = fields.Many2one('purchase.order',string="Purchase")
    partner_obj = fields.Many2one('res.partner',string="Partners")
    sale_order_id = fields.Many2one("sale.order",string="sale order")
    purchase_state =fields.Boolean("purchase_state")
    purchase_count = fields.Integer(string="Purchase Count",compute='compute_purchase_id')
    total_discount = fields.Float(string='Total Discount', store=True)
    test = fields.Boolean("Test 1")
    users = fields.Many2many('res.users',string='users',required=True,groups="practice.approval_group_view")
    discount_apply_to = fields.Selection([
                            ('order_line','Order Line'),
                            ('global','Global')],string="Discount Apply To")
    discount = fields.Float("Discount")
    discount_method = fields.Selection([
        ('fixed','Fixed'),
        ('percentage','Percentage')],string="Discount Method")
    discount_amount = fields.Monetary("Discount Amount")
    quotation = fields.Text(string='Quotation')
    sale_order = fields.Text(string='Sale Order')

    @api.model
    def test_cron_job(self):
        print("\n\n\nScheduled action::\n\n\n")

    # @api.onchange('partner_id')
    # def onchange_partner_id(self):
    #     print("\n\n\n\n\nOnchange::::\n\n\n\n")
    #     if self.partner_id:
    #         print("Partner id")
    #         body = _('This customer has been changed to %s.', self.partner_id.name)
            # self.message_post(body=body)
            # self.message_post(body="This customer has been changed to %s." % (self.partner_id.name))
            # self.message_post(attachment_ids=[attachment.id])




    def action_confirm(self):
        self.name = self.name.replace('SQT','SO')
        return super(SaleOrder,self).action_confirm()

    def action_cancel(self):
        if 'SO' in self.name:
            self.name = self.name.replace('SO','Cancelled')
        else:
            self.name = self.name.replace('SQT','Cancelled')
        return super(SaleOrder,self).action_cancel()

    def action_draft(self):
        self.name = self.name.replace('Cancelled','SQT')
        return super(SaleOrder,self).action_draft()


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
        print("\n\n\n\nValue::::::::::::::::::::::",values)

        if values.get('origin') == False and self._context.get('k'):
            values.pop('origin')

        res = super(SaleOrder,self).write(values)


        if 'partner_id' in values:
            print("\n\n\n\nPartneriddddddddddddddddddddddd----------------")
            self.message_post(body="This customer has been changed to %s." % (self.partner_id.name))

        # for rec in self.order_line:
        #     print("\n\n\nrecccccc--------------------------------",rec)
        #     if rec.product_uom_qty:
        #         print("\n\n\n\nQuantity-----------------")
        #         self.message_post(body="This product %s quantity has been changed to %s." % (rec.product_id.name,rec.product_uom_qty))


        return res


    @api.depends('order_line.product_uom_qty')
    def compute_quantity(self):
        self.quantity = 0
        for rec in self.order_line:
            self.quantity += rec.product_uom_qty

    def merge_record(self):
        order_id = list(rec for rec in self.order_line)
        record_copy = order_id.copy()
        for rec in order_id:
            for res in record_copy:
                if rec != res :
                    if rec.product_id == res.product_id:
                        rec.product_uom_qty += res.product_uom_qty
                        res.unlink()
                        record_copy.remove(res)
                        order_id.remove(res)


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

    def add_pricelist(self):
        print("ADD")
        price_list_name = f"{self.partner_id.name} PriceList"

        price_list = self.env['product.pricelist'].create({
            'name': price_list_name,
            })

        for lines in self.order_line:
            price_line = self.env['product.pricelist.item'].create({
                'product_tmpl_id':lines.product_template_id.id,
                'min_quantity':lines.product_uom_qty,
                'fixed_price':lines.price_unit,
                'pricelist_id':price_list.id,

                })


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
   

    def purchase_order_line(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order Lines',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain':[('sale_order_id','=',self.id)],
        }
        return action
     # ---------------------------------------------------------------
    # def _get_invoiceable_lines(self, final=False):
    #     res = super()._get_invoiceable_lines(final=False)
    #     lines=list(rec.id for rec in res if rec.hide == False)
    #     return self.env['sale.order.line'].browse(lines)

    def _get_invoiceable_lines(self, final=False):
        res = super()._get_invoiceable_lines(final=False)
        return res.filtered(lambda r: not r.hide)
        # return res.filtered(lambda r: r.hide == False)

    # -------------------------------------------------------------------

    def action_send_mail(self):
        template_id = self.env.ref('practice.salary_attechment_email_invite')
        attch = self.env['ir.attachment'].search([
            ('res_model', '=', 'sale.order'), 
            ('res_id', '=', self.id)])
        template_id.send_mail(self.id,force_send=True,email_values={'attachment_ids': [(6, 0, attch.ids)]})
        return True

    # def mail_partner(self):
    #     for record in self.order_line:
    #         vals = {
    #             'subject': record.order_id.partner_id.email,
    #             'body_html': "Dear %s,\n\nThis product %s quantity has been changed to %s." % (record.order_id.partner_id.name,record.product_template_id.name,record.product_uom_qty),
    #             'email_to': record.order_id.partner_id.email,
    #             'email_cc': 'qux@example.com',
                # 'auto_delete': False,
    #             'email_from': 'khushi.d.erpharbor@gamil.com',
    #         }

    #         mail_id = self.env['mail.mail'].sudo().create(vals)
    #         mail_id.sudo().send()

    def mail_partner(self):
        partner_emails = {}
        for record in self.order_line:
            partner_id = record.order_id.partner_id
            partner_emails.setdefault(partner_id, []).append({
                'product_name': record.product_template_id.name,
                'quantity': record.product_uom_qty
            })

        for partner, products in partner_emails.items():
            product_lines = "\n".join("- %s: %s" % (product['product_name'], product['quantity']) for product in products)
            vals = {
                'subject': partner.email,
                'body_html': f"Dear {partner.name},\n\nThis is to inform you about the following changes in your order:\n\n{product_lines}",
                'email_to': partner.email,
                'email_cc': 'qux@example.com',
                'auto_delete': False,
                'email_from': 'khushi.d.erpharbor@gamil.com',
            }

            self.env['mail.mail'].sudo().create(vals).sudo().send()



    # def mail_partner(self):
    #     partner_emails = {}
    #     for record in self.order_line:
    #         partner_id = record.order_id.partner_id
    #         if partner_id not in partner_emails:
    #             partner_emails[partner_id] = []

    #         partner_emails[partner_id].append({
    #             'product_name': record.product_template_id.name,
    #             'quantity': record.product_uom_qty
    #         })

    #     for partner, products in partner_emails.items():
    #         product_lines = ""
    #         for product in products:
    #             product_lines += "- %s: %s\n" % (product['product_name'], product['quantity'])

    #         vals = {
    #             'subject': partner.email,
    #             'body_html': "Dear %s,\n\nThis is to inform you about the following changes in your order:\n\n%s" % (partner.name, product_lines),
    #             'email_to': partner.email,
    #             'email_cc': 'qux@example.com',
    #             'auto_delete': False,
    #             'email_from': 'khushi.d.erpharbor@gamil.com',
    #         }

    #         mail_id = self.env['mail.mail'].sudo().create(vals)
    #         mail_id.sudo().send()

    
    




class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount_amount = fields.Float("Discount Value")
    test_2 = fields.Boolean("Test 2")
    hide = fields.Boolean("Hide")
    discount_method = fields.Float("Discount Method")
    discount_amounts = fields.Float("Discount Amount")

    # @api.model
    # def create(self,vals):
    #     print("\n\n\n\nVals:::::::",vals)
    #     if vals.get('hide'):
    #         vals['invoice_status'] = ''
    #     return super(SaleOrderLine,self).create(vals)

    # def create_invoices(self):
    #     print("\n\n\n\ninvoice:::::::::::::::")
    #     res = super(SaleOrder, self)._create_invoices()
        # records = self.env['sale.order.line'].search([]).filter(lambda line: line.hide)
        # records = self.env['sale.order.line'].filter(lambda r: r.hide == True)
        # records.write({'invoice_status': 'no'})
        # return res

    def write(self,vals):
        print("\n\n\n\nvals::::::::::::::::::::::::::::::::::::::::",vals)
        res = super(SaleOrderLine, self).write(vals)
        if 'product_uom_qty' in vals:
            print("\n\n\n\nQuantity-----------------")
            new_qty = vals.get('product_uom_qty')
            self.order_id.message_post(body="This product %s quantity has been changed to %s." % (self.product_id.name,new_qty))
        return res








        
