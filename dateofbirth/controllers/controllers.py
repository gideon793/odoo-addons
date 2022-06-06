# -*- coding: utf-8 -*-
from odoo import http

# class Dateofbirth(http.Controller):
#     @http.route('/dateofbirth/dateofbirth/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dateofbirth/dateofbirth/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dateofbirth.listing', {
#             'root': '/dateofbirth/dateofbirth',
#             'objects': http.request.env['dateofbirth.dateofbirth'].search([]),
#         })

#     @http.route('/dateofbirth/dateofbirth/objects/<model("dateofbirth.dateofbirth"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dateofbirth.object', {
#             'object': obj
#         })