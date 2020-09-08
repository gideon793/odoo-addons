# -*- coding: utf-8 -*-
from odoo import http

# class Schemes(http.Controller):
#     @http.route('/schemes/schemes/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/schemes/schemes/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('schemes.listing', {
#             'root': '/schemes/schemes',
#             'objects': http.request.env['schemes.schemes'].search([]),
#         })

#     @http.route('/schemes/schemes/objects/<model("schemes.schemes"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('schemes.object', {
#             'object': obj
#         })