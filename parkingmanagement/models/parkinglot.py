# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class parkinglot(models.Model):
    _name = "parking.lot"
    _description = "Parking Lot"

    name = fields.Char(string='Name', required = True)
    _sql_constraints = [
        ('unique_tag_name', 'unique(name)',
         'Duplicate information!'),
    ]
    image=fields.Image(string="Image")
    vehicle_ids = fields.One2many('parking.details', 'parkinglot_id', required = True)
    ticket_ids = fields.One2many('parking.ticket', 'parkinglot_id', required = True)
    ticket_count = fields.Integer(string="ticket count", compute="_compute_ticket")
    operating_time = fields.Many2one(
        'resource.calendar', 'Working Hours')

    def action_list(self):
        action = self.env.ref('parkingmanagement.action_parking_ticket').read()[0]
        return action

    def action_view_ticket(self):


        action = self.env['ir.actions.act_window']._for_xml_id('parkingmanagement.action_parking_ticket')
        action['domain'] = [('parkinglot_id.id', '=', self.id)]
        action['context'] = {
            'default_parkinglot_id': self.id,
            'search_default_filter_state': 1,
        }
        return action

    @api.depends('ticket_ids')
    def _compute_ticket(self):
        self.ticket_count = len(self.ticket_ids)
