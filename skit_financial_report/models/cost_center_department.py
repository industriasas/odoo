# -*- coding: utf-8 -*-

from odoo import models, fields

class CostCenter(models.Model):
    _name = "tf.cost.center"

    name = fields.Char('Cost Center')
    # department_ids = fields.One2many('tf.department', 'cost_center_id', string='Department')

class Department(models.Model):
    _name = "tf.department"

    name = fields.Char('Department')
    # cost_center_id = fields.Many2one('tf.cost.center')