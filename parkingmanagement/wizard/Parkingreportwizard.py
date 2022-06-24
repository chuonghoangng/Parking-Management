# -*- coding: utf-8 -*-
import datetime

from odoo import api, fields, models, _
from datetime import datetime


class Parkingreportwizard(models.TransientModel):
    _name = "parking.report.wizard"
    _description = "Parking report wizard"

    parkinglot_id = fields.Many2one(comodel_name='parking.lot', string="Parking Lot")
    vehicle_id = fields.Many2one(comodel_name='parking.vehicle', string="Vehicle")
    from_date = fields.Datetime(string="From date")
    to_date = fields.Datetime(string="To date")

    @api.model
    def default_get(self, fields):
        res = super(Parkingreportwizard, self).default_get(fields)

        res['from_date'] = datetime.now()
        res['to_date'] = datetime.now()
        return res

    def get_report_data(self):


        domain = []
        if self.parkinglot_id:
            domain = domain + [('parkinglot_id', '=', self.parkinglot_id.id)]
        if self.vehicle_id:
            domain = domain + [('vehicle_id', '=', self.vehicle_id.id)]
        if self.from_date:
            domain = domain + [('time_in', '>=', self.from_date)]
        if self.to_date:
            domain = domain + [('time_in', '<=', self.to_date)]

        tickets = self.env['parking.ticket'].search(domain)

        data = {
            'form': self.read()[0],
            'parkinglot': self.parkinglot_id.name,
            'vehicle': self.vehicle_id.name,
        }
        return tickets, data

    def print_pdf(self):

        return self.env.ref('parkingmanagement.report_pdf_card').report_action(self)

    def print_xlsx(self):
        return self.env.ref('parkingmanagement.report_card_xls').report_action(self)