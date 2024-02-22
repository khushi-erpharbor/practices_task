from odoo import models, fields, api


class Project(models.Model):
     _inherit = "project.project"

     hours_total = fields.Float(string='Hours Project')
     hours_total_planned = fields.Float(string='Scheduled Hours',store=True)
     planning_line_ids = fields.One2many('project.planning.line', inverse_name='project_id',string = 'Planning Hours')


    # @api.depends('hours_total', 'planning_line_ids.hours_invested')
    # def compute_hours_total(self):
    #   print(":::::::::::::::::::::::::::::")