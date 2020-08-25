# -*- coding: utf-8 -*-
from odoo import http

# class Appointment(http.Controller):
#     @http.route('/appointment/appointment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/appointment/appointment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('appointment.listing', {
#             'root': '/appointment/appointment',
#             'objects': http.request.env['appointment.appointment'].search([]),
#         })

#     @http.route('/appointment/appointment/objects/<model("appointment.appointment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('appointment.object', {
#             'object': obj
#         })