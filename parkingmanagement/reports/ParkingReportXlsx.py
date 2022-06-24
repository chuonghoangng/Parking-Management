from odoo import models, _,api, fields
from datetime import datetime, timedelta

class parkinglotcardreport_Xlsx(models.AbstractModel):
    _name = 'report.parkingmanagement.report_xls'
    _inherit = 'report.report_xlsx.abstract'

    def _convert_datetime(self,utctime):
        return fields.Datetime.context_timestamp(self, utctime)
    def generate_xlsx_report(self, workbook, data, wizard):

        tickets, data = wizard.get_report_data()
        print("tickets",tickets)

        sheet = workbook.add_worksheet("Report ticket")
        bold = workbook.add_format({'bold': True})
        form1 = workbook.add_format({'align': 'right'})
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 30)
        sheet.set_column('D:D', 25)

        row = 1
        col = 1

        sheet.write(0, 1, _("REPORT ON PARKING"), bold)
        sheet.write(row, col, "Code", bold)
        sheet.write(row, col + 1, "Start time ", bold)
        sheet.write(row, col + 2, "Into money", bold)
        total = sum(t.totals for t in tickets)
        sum_ticket = len(tickets)
        for ticket in tickets:
            row += 1
            sheet.write(row, col, ticket.code)
            sheet.write(row, col + 1, str(self._convert_datetime(ticket.time_in).strftime('%Y-%m-%d %H:%M:%S')))
            sheet.write(row, col + 2,ticket.totals)
        row += 2
        sheet.write(row, col + 1, "Total traffic (turn)",bold)
        sheet.write(row, col + 2, sum_ticket,form1)
        row += 1
        sheet.write(row, col + 1, "Total amount (VND)",bold)
        sheet.write(row, col + 2, total,form1)

