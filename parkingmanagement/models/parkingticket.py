from odoo import api, fields, models, _
from datetime import datetime, date
from odoo.exceptions import  ValidationError


class parkingticket(models.Model):
    _name = "parking.ticket"
    _description = "Parking Ticket"
    # THUOC TINH
    image = fields.Image(string="Image")
    code = fields.Char(string='Code', tracking=True, default="New")
    # thời gian vào bãi xe
    time_in = fields.Datetime(string="Start time", default=fields.Datetime.now)
    parking_time = fields.Float(string='Parking time', default=0)
    ref = fields.Char(string='Notification', compute='_compute_check_ticket')
    # KHOA NGOAI
    parkinglot_id = fields.Many2one(comodel_name='parking.lot', string="Parking Lot", required=True)
    vehicle_id = fields.Many2one(comodel_name='parking.vehicle', string="Vehicle", required=True)
    state = fields.Selection([
        ('draft', 'Unpaid'),
        ('done', 'Done')
    ], default='draft', string="Status", required=True)

    totals = fields.Float(string="Total:", default=0)

    # TAO MA CODE CHO MUOI LUONG XE VAO BAI GIU XE
    @api.model
    def create(self, vals):
        res = super(parkingticket, self).create(vals)

        if vals.get('parkinglot_id') and vals.get('vehicle_id'):
            for x in res:
                detail = x.parkinglot_id.vehicle_ids.filtered(lambda v: v.vehicle_id.id == vals.get('vehicle_id'))
                if detail:
                    same_categ_tickets = x.parkinglot_id.ticket_ids.filtered(
                        lambda t: t.vehicle_id.id == vals.get('vehicle_id'))
                    if detail.number <= len(same_categ_tickets):
                        raise ValidationError(_("Full load"))
                    list = x.parkinglot_id.operating_time.attendance_ids
                    # CHECK THOI GIAN VAO BAI CO HOP LE KHONG
                    time_in = self._convert_datetime(x.time_in)
                    checktime = False
                    for listtime in list:
                        if time_in.weekday() == int(
                                listtime.dayofweek) and time_in.hour >= listtime.hour_from and time_in.hour < listtime.hour_to:
                            checktime = True
                    if not checktime:
                        raise ValidationError(_("The time to enter the parking lot is not at the prescribed time!"))
                else:
                    raise ValidationError(_("This vehicle is not available in the parking lot - No space"))
        else:
            raise ValidationError(_("Please enter full information!"))
        res.code = self.env['ir.sequence'].next_by_code('parking.ticket')
        return res

    def write(self, vals):
        if not self.code and not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('parking.ticket')
        return super(parkingticket, self).write(vals)

    @api.depends('vehicle_id', 'parkinglot_id', 'time_in')
    def _compute_check_ticket(self):

        a = ""
        b = ""
        c = "The time to enter the parking lot is not at the prescribed time!"

        for ticket in self:

            if ticket.vehicle_id and ticket.parkinglot_id:
                detail = ticket.parkinglot_id.vehicle_ids.filtered(lambda v: v.vehicle_id == ticket.vehicle_id)

                if detail:
                    same_categ_tickets = ticket.parkinglot_id.ticket_ids.filtered(
                        lambda t: t.vehicle_id == ticket.vehicle_id)
                    if detail.number > len(same_categ_tickets):
                        b = "There's room left"
                    else:
                        b = "Full load"
                    a = "There is this type of vehicle in the parking lot"
                else:
                    a = "This vehicle is not available in the parking lot"
                    b = "Full load"

                # kiểm tra xem thời gian vào bãi gửi xe có đúng thời gian quy định hay không
                list = ticket.parkinglot_id.operating_time.attendance_ids
                time_in = self._convert_datetime(ticket.time_in)
                for x in list:
                    if time_in.weekday() == int(
                            x.dayofweek) and time_in.hour >= x.hour_from and time_in.hour < x.hour_to:
                        c = "Valid entry time"
                ticket.ref = a + " - " + b + " - " + c
            else:
                ticket.ref = "Please select the type of vehicle and the parking lot"

    def _convert_datetime(self, utctime):
        return fields.Datetime.context_timestamp(self, utctime)

    def action_payment(self):
        for rec in self:
            today = datetime.now()
            if rec.time_in:
                t_diff = (today - rec.time_in).total_seconds()
                if (t_diff % 3600) >= 1800:
                    hours = divmod(t_diff, 3600)[0] + 1
                else:
                    hours = divmod(t_diff, 3600)[0]
                rec.parking_time = hours
            else:
                rec.parking_time = 0
            t1 = date(year=rec.time_in.year, month=rec.time_in.month, day=rec.time_in.day)
            t2 = date(year=today.year, month=today.month, day=today.day)

            if (t1 == t2):
                item = rec.vehicle_id.price
                rec.totals = item
            else:
                price = rec.vehicle_id.price
                mulct = rec.vehicle_id.mulct
                delta = abs(t2 - t1)

                rec.totals = price * (int(delta.days) + 1) + mulct * int(delta.days)
            if rec.state == 'draft':
                rec.state = 'done'
