# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class parkingdetails(models.Model):
    _name = "parking.details"
    _table = "parking_details"
    _description = "Parking details"

    #THUOC TINH
    number = fields.Integer(string='Limit', required = True)
    #KHOA NGOAI VOI THE LOAI
    parkinglot_id = fields.Many2one(comodel_name='parking.lot', string="Parking Lot", required = True)
    vehicle_id = fields.Many2one(comodel_name='parking.vehicle', string="Vehicle", required = True)
    _sql_constraints = [
        ('unique_tag_name', 'unique(parkinglot_id,vehicle_id)', 'Duplicate information, there is information about this parking lot and type of vehicle'),
    ]


