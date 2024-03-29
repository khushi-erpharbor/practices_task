from odoo import api, fields, models
from odoo.exceptions import ValidationError 


class BulkUpload(models.TransientModel):
    _name = 'quotation.bulk.upload'


    product_line_ids = fields.One2many('quotation.bulk.upload.line','upload_line',string='Product Line')



    # def upload_record(self):
    #     print("\n\n\nuplolad record")
    #     ctx = self.env.context
    #     so = self.env['sale.order'].browse(ctx.get('active_id'))
    #     line = []
    #     for record in self.product_line_ids:
    #         for rec in record.product_ids:
    #             so.update({
    #                 'order_line': [(fields.Command.create({'product_uom_qty':record.quantity,'product_id':rec.id}))]
    #             })
                

    def upload_record(self):
        print("\n\n\nupload record")
        ctx = self.env.context
        so = self.env['sale.order'].browse(ctx.get('active_id'))
        line_vals = []
        for record in self.product_line_ids:
            for rec in record.product_ids:
                line_vals.append((0, 0, {
                    'product_uom_qty': record.quantity,
                    'product_id': rec.id
                }))
        so.write({'order_line': line_vals})



class BulkUploadLine(models.TransientModel):
    _name = 'quotation.bulk.upload.line'

    product_ids = fields.Many2many("product.product",string="Product")
    quantity = fields.Float("Quantity",default='1')
    upload_line = fields.Many2one('quotation.bulk.upload',string="Upload Line")



    @api.constrains('quantity')
    def check_product_quantity(self):
        print("check")
        for record in self:
            if record.quantity <= 0.0:
                raise ValidationError("Quantity should not be 0 or negative.")



