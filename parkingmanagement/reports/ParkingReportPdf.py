from odoo import api, fields, models
from datetime import datetime, timedelta

class parkinglotcardreport(models.AbstractModel):
    _name = 'report.parkingmanagement.report_pdf'
    def _convert_datetime(self,utctime):
        return fields.Datetime.context_timestamp(self, utctime)
    def _get_report_values(self, docid, data=None):
        wizard = self.env['parking.report.wizard'].browse(docid)
        tickets, data = wizard.get_report_data()

        print("tickets",tickets)
        return {
            'doc_ids': tickets.ids,
            'doc_model': "parking.ticket",
            'docs': tickets,
            'data': data,
            'vehicle': data['vehicle'],
            'parkinglot': data['parkinglot'],
            'display_datetime': lambda dt: self._convert_datetime(dt).strftime('%Y-%m-%d %H:%M:%S')
        }
