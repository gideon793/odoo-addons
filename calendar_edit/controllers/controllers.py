# -*- coding: utf-8 -*-
from odoo import http

# class CalendarEdit(http.Controller):
#     @http.route('/calendar_edit/calendar_edit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/calendar_edit/calendar_edit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('calendar_edit.listing', {
#             'root': '/calendar_edit/calendar_edit',
#             'objects': http.request.env['calendar_edit.calendar_edit'].search([]),
#         })

#     @http.route('/calendar_edit/calendar_edit/objects/<model("calendar_edit.calendar_edit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('calendar_edit.object', {
#             'object': obj
#         })