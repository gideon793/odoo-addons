from odoo import models, fields, api

class waitinglist(models.Model):
    _name = 'waitinglist.waitinglist'
    name = fields.Many2one('res.partner', string='Patient Name')
    dateadded = fields.Date('Date Added', default=fields.Date.today())
    providerlink = fields.Many2one('doctors.doctors', string='Doctor')
    registration = fields.Char(related='name.registration',store=True)
    phone = fields.Char(related='name.mobile', store=True)
    admitted = fields.Boolean(string='Patient admitted')
    address = fields.Char(related='name.contact_address')
    age= fields.Integer(related='name.agecal')
    
class psychotics(models.Model):
    _name = 'waitinglist.substance'
    name = fields.Many2one('res.partner', string='Patient Name')
    dateadded = fields.Date('Date Added', default=fields.Date.today())
    providerlink = fields.Many2one('doctors.doctors', string='Doctor')
    registration = fields.Char(related='name.registration',store=True)
    phone = fields.Char(related='name.mobile', store=True)
    admitted = fields.Boolean(string='Patient admitted')
    address = fields.Char(related='name.contact_address')
    age= fields.Integer(related='name.agecal')

class otherwait(models.Model):
    _name = 'waitinglist.otherwait'
    name = fields.Many2one('res.partner', string='Patient Name')
    dateadded = fields.Date('Date Added', default=fields.Date.today())
    providerlink = fields.Many2one('doctors.doctors', string='Doctor')
    registration = fields.Char(related='name.registration',store=True)
    phone = fields.Char(related='name.mobile', store=True)
    admitted = fields.Boolean(string='Patient admitted')
    address = fields.Char(related='name.contact_address')
    age= fields.Integer(related='name.agecal')


class othersub(models.Model):
    _name = 'waitinglist.othersub'
    name = fields.Many2one('res.partner', string='Patient Name')
    dateadded = fields.Date('Date Added', default=fields.Date.today())
    providerlink = fields.Many2one('doctors.doctors', string='Doctor')
    registration = fields.Char(related='name.registration',store=True)
    phone = fields.Char(related='name.mobile', store=True)
    admitted = fields.Boolean(string='Patient admitted')
    address = fields.Char(related='name.contact_address')
    age= fields.Integer(related='name.agecal')

