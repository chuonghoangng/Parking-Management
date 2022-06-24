# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class parkingvehicle(models.Model):
    _name = "parking.vehicle"
    _description = "parking vehicle"
    name = fields.Char(string='Name', required = True)
    price = fields.Integer(string='price',default=0, required = True)

    mulct = fields.Float(string="Mulct",default=0, required = True)
    _sql_constraints = [
        ('unique_tag_name', 'unique(name)',
         'Duplicate information!'),
    ]


