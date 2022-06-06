# -*- coding: utf-8 -*-
from odoo import http

# class Diagnosis(http.Controller):
#     @http.route('/diagnosis/diagnosis/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/diagnosis/diagnosis/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('diagnosis.listing', {
#             'root': '/diagnosis/diagnosis',
#             'objects': http.request.env['diagnosis.diagnosis'].search([]),
#         })

#     @http.route('/diagnosis/diagnosis/objects/<model("diagnosis.diagnosis"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('diagnosis.object', {
#             'object': obj
#         })