from odoo import api, fields, models


class parkingpricelist(models.Model):
    _name = "parking.pricelist"
    _description = "Parking price list"

    id = fields.Integer(string="ID", required = True)
    name = fields.Char(string="Name", required = True)
    vehicle_ids = fields.Many2many('parking.vehicle',string="List vehicle")
    _sql_constraints = [
        ('unique_tag_name', 'unique(name)',
         'Duplicate information!'),
    ]
