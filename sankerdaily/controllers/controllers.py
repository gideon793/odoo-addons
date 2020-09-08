# -*- coding: utf-8 -*-
from odoo import http

# class Sankerdaily(http.Controller):
#     @http.route('/sankerdaily/sankerdaily/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sankerdaily/sankerdaily/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sankerdaily.listing', {
#             'root': '/sankerdaily/sankerdaily',
#             'objects': http.request.env['sankerdaily.sankerdaily'].search([]),
#         })

#     @http.route('/sankerdaily/sankerdaily/objects/<model("sankerdaily.sankerdaily"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sankerdaily.object', {
#             'object': obj
#         })