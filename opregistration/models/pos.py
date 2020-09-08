# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime,date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class posorderedit(models.Model):
    _inherit = 'pos.order'
    _name = 'pos.order'
    date = fields.Date('Order Date')

    @api.onchange('date_order'):
    def _date(self):
        for record in self:
            if record.date_order:
                dt=str(record.date_order)
                record.date=datetime.strptime(dt, "%Y-%m-%d").date()

