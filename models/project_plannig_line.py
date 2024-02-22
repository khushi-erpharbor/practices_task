from odoo import fields, models, api


class ProjectPlanningLine(models.Model):
    _name = 'project.planning.line'
    _description = 'Project Planning Line'

    project_id = fields.Many2one(comodel_name='project.project', string='Project')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    hours_invested = fields.Float(string='Hour Invested', store=True)
    hours_assigned = fields.Float(string='Hour Assign')  # invisible
    hours_assigned_string = fields.Char(string='Hour Assigned',store=True)
    hours_pending = fields.Float(string='Hour Pending')  # invisible
    hours_pending_string = fields.Char(string='Hour Pending String')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    hours_assigned = fields.Float(string='H.Assigned')
