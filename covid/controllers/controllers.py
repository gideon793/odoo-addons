# -*- coding: utf-8 -*-
from odoo import http

# class Covid(http.Controller):
#     @http.route('/covid/covid/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/covid/covid/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('covid.listing', {
#             'root': '/covid/covid',
#             'objects': http.request.env['covid.covid'].search([]),
#         })

#     @http.route('/covid/covid/objects/<model("covid.covid"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('covid.object', {
#             'object': obj
#         })