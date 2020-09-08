# -*- coding: utf-8 -*-
from odoo import http

# class Sankeremployee(http.Controller):
#     @http.route('/sankeremployee/sankeremployee/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sankeremployee/sankeremployee/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sankeremployee.listing', {
#             'root': '/sankeremployee/sankeremployee',
#             'objects': http.request.env['sankeremployee.sankeremployee'].search([]),
#         })

#     @http.route('/sankeremployee/sankeremployee/objects/<model("sankeremployee.sankeremployee"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sankeremployee.object', {
#             'object': obj
#         })