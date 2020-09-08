# -*- coding: utf-8 -*-
from odoo import http

# class Inpatient(http.Controller):
#     @http.route('/inpatient/inpatient/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inpatient/inpatient/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inpatient.listing', {
#             'root': '/inpatient/inpatient',
#             'objects': http.request.env['inpatient.inpatient'].search([]),
#         })

#     @http.route('/inpatient/inpatient/objects/<model("inpatient.inpatient"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inpatient.object', {
#             'object': obj
#         })