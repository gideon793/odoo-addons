# -*- coding: utf-8 -*-
from odoo import http

# class Opregistration(http.Controller):
#     @http.route('/opregistration/opregistration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/opregistration/opregistration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('opregistration.listing', {
#             'root': '/opregistration/opregistration',
#             'objects': http.request.env['opregistration.opregistration'].search([]),
#         })

#     @http.route('/opregistration/opregistration/objects/<model("opregistration.opregistration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('opregistration.object', {
#             'object': obj
#         })