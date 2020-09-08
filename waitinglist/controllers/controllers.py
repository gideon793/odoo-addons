# -*- coding: utf-8 -*-
from odoo import http

# class Waitinglist(http.Controller):
#     @http.route('/waitinglist/waitinglist/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/waitinglist/waitinglist/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('waitinglist.listing', {
#             'root': '/waitinglist/waitinglist',
#             'objects': http.request.env['waitinglist.waitinglist'].search([]),
#         })

#     @http.route('/waitinglist/waitinglist/objects/<model("waitinglist.waitinglist"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('waitinglist.object', {
#             'object': obj
#         })