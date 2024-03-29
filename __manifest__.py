{
    "name": "Session Task",
    'version': '16.0.1.0.0',
    'summary': 'Invoices & Payments',
    'sequence': 10,
    'description': """
School Management 
====================
The specific and easy-to-use Invoicing system in Odoo allows you to keep track of your accounting, even when you are not an accountant. It provides an easy way to follow up on your vendors and customers.

You could use this simplified accounting in case you work with an (external) account to keep your books, and you still want to keep track of payments. This module also offers you an easy method of registering payments, without having to encode complete abstracts of account.
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['base','sale','purchase','stock','product','account','project'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/ir_sequence.xml',
        'data/mail_template.xml',
        'data/ir_cron.xml',
        'views/template.xml',
        'wizard/purchase_wizard_views.xml',
        'wizard/purchase_order_wiz_views.xml',
        'wizard/sale_confrom_views.xml',
        'wizard/sale_order_wizard.xml',
        'wizard/action_sale_line.xml',
        'wizard/sale_order_discount_wiz_views.xml',
        'wizard/bulk_upload_wiz_views.xml',
        'views/sale_order_line.xml',
        'views/res_config_settings_views.xml',
        'views/customer_discount_view.xml',
        'views/res_partner_view.xml',
        'views/search_customer_views.xml',
        'views/purchase_order_views.xml',
        'views/purchase_template_view.xml',
        'views/project_project_views.xml',
        'views/project_plannig_line_views.xml',
        'report/sale_discount_report.xml',
        'report/sale_inherit_report.xml',
        'report/purchase_inherit_report.xml',
        'report/sale_discount_report.xml',
        'report/product_template_report.xml',
        'report/customer_report.xml',
        'report/sale_global_dis.xml',
        
        # 'data/action_server.xml'


    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
