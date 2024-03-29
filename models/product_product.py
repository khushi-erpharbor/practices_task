from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _name_search(self,name,args=None,operator="",limit=100,name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('barcode', operator, name),('name', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
    