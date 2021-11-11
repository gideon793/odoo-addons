# -*- coding: utf-8 -*-
from odoo import http

# class Endoscopy(http.Controller):
#     @http.route('/endoscopy/endoscopy/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/endoscopy/endoscopy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('endoscopy.listing', {
#             'root': '/endoscopy/endoscopy',
#             'objects': http.request.env['endoscopy.endoscopy'].search([]),
#         })

#     @http.route('/endoscopy/endoscopy/objects/<model("endoscopy.endoscopy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('endoscopy.object', {
#             'object': obj
#         })