from odoo import http
from odoo.http import request


class WelcomeEhcs(http.Controller):


    @http.route([
        '/welcome_ehcs',
    ], type='http', auth="public", website=True)
    def welcome_ehcs(self,):
        print("\n\n\nwelcome")

        country = request.env["res.country"].sudo().search([])
      
        value = {
            'user':request.env.user,
            'country':country,
        }
        return request.render("practice.welcome_ehcs",value)


    @http.route([
        '/create_portal_partner',
    ], type='http', auth="public", website=True)
    def create_portal_partner(self):
        print("\n\n\ncreate_portal_partner")

        country = request.env["res.country"].sudo().search([])
        value = {
            'country':country,
        }

        return request.render("practice.portal_partner",value)


    @http.route([
        '/view_portal_partner',
    ], type='http', auth="public", website=True)
    def view_portal_partner(self):
        print("\n\n\nview_portal_partner")
        partner = request.env['res.partner'].sudo().search([])
        value ={
            'partner':partner,
        }

        return request.render("practice.portal_partner_con",value)

    @http.route([
        '/view_only_portal_partner',
    ], type='http', auth="public", website=True)
    def view_only_portal_partner(self):
        print("\n\n\nview_only_portal_partner::::::::::::::::::")

        # partner = request.env['res.partner'].search([('portal_partner','=',True)])
       
        return request.render("practice.thanks_msg")




    @http.route(['/create_partner'],type='http', auth="public", website=True)
    def create_partner(self,**post):

        name = post.get('name')
        phone = post.get('phone')
        email = post.get('email')
        country_id = post.get('country')

        partner = request.env['res.partner'].create({
        'name':name,
        'phone':phone,
        'email':email,
        'country_id':country_id,
        'portal_partner':True
        })

        partners = request.env['res.partner'].search([('portal_partner','=',True)])

        return request.render("practice.portal_partner_only",{'partners': partners,'partner':partner})


    @http.route(['/sale_details'],type='http', auth="public", website=True)
    def sale_details(self,**post):
        print("\n\n\nsale details route call-------------------------")

        sale = request.env['sale.order'].sudo().search([])

        return request.render("practice.sale_detail",{'details': sale})


