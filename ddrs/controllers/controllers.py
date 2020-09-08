# -*- coding: utf-8 -*-
from odoo import http

# class Ddrs(http.Controller):
#     @http.route('/ddrs/ddrs/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ddrs/ddrs/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ddrs.listing', {
#             'root': '/ddrs/ddrs',
#             'objects': http.request.env['ddrs.ddrs'].search([]),
#         })

#     @http.route('/ddrs/ddrs/objects/<model("ddrs.ddrs"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ddrs.object', {
#             'object': obj
#         })