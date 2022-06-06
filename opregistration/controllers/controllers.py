# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Lab(http.Controller):
    @http.route('/lab/lab/', auth='public')
    def index(self, **kw):
        opreg_details = request.env['opregistration'].sudo().search([])
        return request.render('lab.opregistration_page', {'details': opreg_details})


# class Opregistration(http.Controller):
#     @http.route('/opregistration/opregistration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/opregistration/opregistration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('opregistration.listing', {
#             'root': '/opregistration/opregistration',
#             'objects': http.request.env['opregistration.opregistration'].search([]),
#         })

#     @http.route('/opregistration/opregistration/objects/<model("opregistration.opregistration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('opregistration.object', {
#             'object': obj
#         })