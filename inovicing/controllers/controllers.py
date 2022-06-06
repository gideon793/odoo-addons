# -*- coding: utf-8 -*-
from odoo import http

# class Inovicing(http.Controller):
#     @http.route('/inovicing/inovicing/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inovicing/inovicing/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inovicing.listing', {
#             'root': '/inovicing/inovicing',
#             'objects': http.request.env['inovicing.inovicing'].search([]),
#         })

#     @http.route('/inovicing/inovicing/objects/<model("inovicing.inovicing"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inovicing.object', {
#             'object': obj
#         })