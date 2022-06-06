# -*- coding: utf-8 -*-
from odoo import http

# class Outreach(http.Controller):
#     @http.route('/outreach/outreach/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/outreach/outreach/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('outreach.listing', {
#             'root': '/outreach/outreach',
#             'objects': http.request.env['outreach.outreach'].search([]),
#         })

#     @http.route('/outreach/outreach/objects/<model("outreach.outreach"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('outreach.object', {
#             'object': obj
#         })