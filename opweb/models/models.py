# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from fractions import Fraction

class opweb(models.Model):
    _name = 'opweb.opweb'
    _description = 'For front end prescription'
    _rec_name='partner_id'
    partner_id = fields.Many2one('res.partner', string='Patient Name')
    registration = fields.Char(related='partner_id.registration')
    prescription_lines = fields.One2many('opweb.prescriptionlines', 'opweb', string='Prescription Lines')
    doctor = fields.Selection([('ssyiem', 'Dr. S. Syiem'), ('eddie', 'Dr. E. Mukhim'), ('didak', 'Dr. D. Khonglah'),
                               ('gideon', 'Dr. G. Rynjah'), ('rlaloo', 'Dr. R. Laloo'),
                               ('lashngain', 'Dr.  L. Sohliya'), ('dkynjin', 'Dr. D. Kynjin'),
                               ('slahiri', 'Dr. S. Lahiri'), ('vranee', 'Dr. V. Ranee'),
                               ('naphi', 'Naphisabet Kharsati'), ('nongstoin', 'Nongstoin Project'),
                               ('mairang', 'Mairang Project'), ('mawkyrwat', 'Mawkyrwat Project'),
                               ('fatima', 'Fatima Project')], string='Doctor')
    date = fields.Date(string='Date of Appointment', default=fields.Date.today())
    state = fields.Selection([('ordered','Ordered'),('delivered', 'Delivered')])
    service_lines = fields.One2many('opweb.serviceslines', 'opweb', string='Service Lines')
    roundOff = fields.Float('Round off')
    consultation = fields.Float('Consultation Charge')
    registration_charge = fields.Float('Registration Charge')
    opregNo = fields.Char('Opreg ID')
    payment = fields.Float('Payment')

class  serviceslines(models.Model):
    _name= 'opweb.serviceslines'
    _rec_name = 'service'
    service = fields.Many2one('product.product', string='Service')
    service_charge = fields.Float('Service Charge')
    opweb = fields.Many2one('opweb.opweb', string='OpWeb')


class prescriptionlines(models.Model):
    _name = 'opweb.prescriptionlines'
    _rec_name = 'med_name'
    medicine = fields.Many2one('product.product', string='Product')
    med_name = fields.Char('Medicine Name')
    ordered_no = fields.Integer('Total No. Ordered')
    medicine_lines = fields.One2many('opweb.medicinelines', 'prescription', string='Medication Lines')
    opweb = fields.Many2one('opweb.opweb', string='OpWeb')
    type = fields.Char(default='product')


class medicinelines(models.Model):
    _name = 'opweb.medicinelines'
    _rec_name='frequency'
    prescription = fields.Many2one('opweb.prescriptionlines')
    dose = fields.Float('Dosage')
    units = fields.Selection([(1, 'tablet'), (2, 'ml'), (3, 'drops'), (4, 'puffs'), (5, 'patch'), (6, 'ampuole'),(7, 'spoons'),(8, 'local application')], string='Units')
    frequency = fields.Selection([(1,'once daily'),(2,'twice daily'),(3, 'thrice daily'),(4, 'four times a day'),(5, 'five times a day'),(6, 'once daily at bedtime'),(7,'when required'),(8, 'immediately'),(9, 'Others')])
    duration = fields.Integer('Number of days')
    special = fields.Char('Special Instructions')
    total = fields.Integer(compute='_tot',string='Total Number of Tablets')
    dose_fraction = fields.Char('Dosage in fractions', compute='_dosefraction')

    @api.onchange('dose')
    def _dosefraction(self):
        for record in self:
            record.dose_fraction = str(Fraction(record.dose))

    @api.model
    def _tot(self):
        for record in self:
            if record.frequency != 6:
                record.total = record.dose * record.frequency * record.duration
            else:
                record.total = 0

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        imediate_obj=self.env['stock.immediate.transfer']
        res=super(SaleOrder,self).action_confirm()
        for order in self:
            warehouse=order.warehouse_id
            if warehouse.is_delivery_set_to_done and order.picking_ids: 
                for picking in self.picking_ids:
                    picking.action_confirm()
                    picking.action_assign()


                    imediate_rec = imediate_obj.create({'pick_ids': [(4, order.picking_ids.id)]})
                    imediate_rec.process()
                    if picking.state !='done':
                        for move in picking.move_ids_without_package:
                            move.quantity_done = move.product_uom_qty
                        picking.button_validate()
            self._cr.commit()

            if warehouse.create_invoice and not order.invoice_ids:
                order.action_invoice_create()  

            if warehouse.validate_invoice and order.invoice_ids:
                for invoice in order.invoice_ids:
                    invoice.action_invoice_open()

        return res

class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"
    is_delivery_set_to_done = fields.Boolean(string="Is Delivery Set to Done")
    create_invoice=fields.Boolean(string='Create Invoice?')
    validate_invoice = fields.Boolean(string='Validate invoice?')