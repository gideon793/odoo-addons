# -*- coding: utf-8 -*-
from asyncio.log import logger
from odoo import http
from odoo.http import request
from datetime import datetime, date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import logging
import json

_logger = logging.getLogger(__name__)

class Opweb(http.Controller):
    @http.route('/opweb/opweb', auth='public', website=True)
    def index(self, **post):
        return request.render('opweb.opreg_doctor', {})

    @http.route('/opweb/doc_submit', auth='public', website=True)
    def doc_submit(self, **post):
        _logger.info(post.get('doctor'))
        op_details = request.env['opregistration'].sudo().search([['doctor','=', post.get('doctor')],['date','=', date.today().strftime(DATE_FORMAT)]])
        medications = request.env['product.product'].sudo().search([['type','=','product']])
        return request.render('opweb.opreg_details', {'op_details':op_details, 'medications': medications, 'title': 'SAN-KER Prescription', 'doctor': post.get('doctor'), 'datePres': date.today().strftime(DATE_FORMAT)})

    @http.route('/opweb/submit', auth='public', website=True, csrf=False, type='json')
    def sumbit(self, **post):
        postdata = json.loads(request.httprequest.data)
        return http.request.env['ir.ui.view'].render_template('opweb.test_page', {'params': postdata})
    
    @http.route('/opweb/prescription', auth='public', csrf=False, type='json')
    def prescription(self, **post):
        prescription_lines = post['prescription']
        pres_lines = []
        for line in prescription_lines:
            det_lines = []
            for det in line['lines']:
                det_lines.append((0,0,{
                    'dose': det['num'],
                    'frequency': det['freq'],
                    'duration': det['duration'],
                    'special': det['special'],
                    'units': det['units']
                }))

            if line['med_id']:
                pres_lines.append((0,0,{
                    'medicine':line['med_id'],
                    'ordered_no': int(float(line['medTotal'])),
                    'med_name': line['name'],
                    'medicine_lines': det_lines,
                    'units': det['units']
                    }))
            else:
                pres_lines.append((0,0, {
                    'med_name': line['name'],
                    'medicine_lines': det_lines,
                    'ordered_no': int(float(line['medTotal']))
                }))

        if request.jsonrequest:
            g = 'res.partner(%s,)' % post['partner_id']
            presDate = datetime.strptime(post['date'], DATE_FORMAT).strftime(DATE_FORMAT)
            rec = request.env['opweb.opweb'].sudo().search([['date','=', presDate], ['partner_id.id','=', post['partner_id']],['doctor','=', post['doctor']]])
            if rec:
                for line in rec.prescription_lines:
                    line.unlink()
                rec.prescription_lines = pres_lines
            else:
                request.env['opweb.opweb'].sudo().create({
                    'partner_id': post['partner_id'],
                    'date': post['date'],
                    'doctor':post['doctor'],
                    'prescription_lines': pres_lines,
                    'state': 'ordered',
                    'opregNo': post['opreg_id']
                })
            return 'success'

    @http.route('/opweb/patdetail', auth='public', csrf=False, type='json')
    def todaypres (self, **post):
        _logger.info(post)
        dt = datetime.strptime(post['date'], DATE_FORMAT).strftime(DATE_FORMAT)
        posPrescriptions = request.env['pos.order'].sudo().search([['partner_id.id','=',post['partner_id']],['config_id.id', '!=', '11']])
        salePrescriptions = request.env['sale.order'].sudo().search([['partner_id.id','=',post['partner_id']]])
        opNewPrescriptions = request.env['opweb.opweb'].sudo().search([['partner_id.id','=',post['partner_id']], ['date','!=', dt]])
        oldPrescriptionDetails = []
        opPrescriptionsDetails = []
        posOldPrescriptions = []
        saleOldPrescriptions = []
        posOldPrescriptions.append(self.oldPrescriptions(posPrescriptions, 'date_order', 'lines', 'qty', 'product_id'))
        saleOldPrescriptions.append(self.oldPrescriptions(salePrescriptions, 'date_order', 'order_line', 'product_uom_qty', 'product_id'))
        opPrescriptionsDetails.append(self.opWebPrescriptions(opNewPrescriptions))
        for detail in opPrescriptionsDetails:
            prescriptionDetails = {}
            for d in detail:
                prescriptionDetails.update({'date': d['date'], 'medLines': d['medLines']})
                oldPrescriptionDetails.append(prescriptionDetails)
        for detail in saleOldPrescriptions:
            for det in detail:
                if filter(lambda date: date['date'] != det['date'], oldPrescriptionDetails):
                    prescriptionDetails = {}
                    prescriptionDetails.update({'date': det['date'], 'medLines': det['medLines']})
                    oldPrescriptionDetails.append(prescriptionDetails)
        for detail in posOldPrescriptions:
            for det in detail:
                if filter(lambda x: x['date'] != det['date'], oldPrescriptionDetails):
                    prescriptionDetails={}
                    prescriptionDetails.update({'date': det['date'], 'medLines': det['medLines']})
                    oldPrescriptionDetails.append(prescriptionDetails)
        pat_det = request.env['opweb.opweb'].sudo().search([['date','=', dt], ['partner_id.id','=', post['partner_id']],['opregNo','=', post['opregId']]])
        med_all = []
        for line in pat_det.prescription_lines:
            meds = {}
            med_name = line.med_name
            medicine = line.medicine
            ordered_no = line.ordered_no
            med_line_all =[]
            for det in line.medicine_lines:
                det_array = {}
                dose = det.dose
                frequency = det.frequency
                duration = det.duration
                special = det.special
                det_array.update({'dose':dose,'duration':duration, 'frequency':frequency, 'special':special})
                med_line_all.append(det_array)
            meds.update({'medName': med_name, 'medicine': medicine, 'medicineQuantity':ordered_no, 'medLines': med_line_all})
            med_all.append(meds)
        return {'prescription_lines': med_all, 'old_prescriptions': oldPrescriptionDetails, 'payment': pat_det.payment}
    
    def oldPrescriptions(self, presEnv, dateFormat, lineFormat, qtyFormat, productIdFormat):
        totalMedOrders = []
        for pres in presEnv:
            presDetails = {}
            date = getattr(pres, dateFormat).strftime(DATE_FORMAT)
            medLines = []
            for line in getattr(pres,lineFormat):
                if getattr(line, productIdFormat).type == 'product':
                    medArray = {}
                    medName = getattr(line, productIdFormat).display_name
                    medicineQuantity = getattr(line, qtyFormat)
                    medArray.update({'medName': medName, 'medicineQuantity': medicineQuantity, 'medLines': ''})
                    medLines.append(medArray)
            if len(medLines) > 0:
                presDetails.update({'date': date, 'medLines': medLines})
                totalMedOrders.append(presDetails)
        return totalMedOrders

    def opWebPrescriptions(self, opweb):
        totalMedOrders = []
        for prescription in opweb:
            presDetails = {}
            medLines = []
            for line in prescription['prescription_lines']:
                if line.type == 'product':
                    medArray = {}
                    medicineLines = []
                    for medDetLine in line['medicine_lines']:
                        medDetLineDetail = {}
                        medDetLineDetail.update({'dose': medDetLine['dose'], 'duration': medDetLine['duration'], 'frequency': medDetLine['frequency'], 'special': medDetLine['special']})
                        medicineLines.append(medDetLineDetail)
                    medArray.update({'medName': line['medicine'].display_name, 'medicineQuantity': line['ordered_no'], 'medicineLines': medicineLines})
                    medLines.append(medArray)
            if len(medLines)>0:
                presDetails.update({'date': prescription['date'].strftime(DATE_FORMAT), 'medLines': medLines})
                totalMedOrders.append(presDetails)
        return totalMedOrders

    @http.route('/opweb/pharmacy', auth='public', website=True)
    def pharmacyMain (self):
        appointments = request.env['opregistration'].sudo().search([['date','=', date.today().strftime(DATE_FORMAT)]])
        medications = request.env['product.product'].sudo().search([['type','=','product']])
        services = request.env['product.product'].sudo().search([['type','=','service']])
        prescriptions = request.env['opweb.opweb'].sudo().search([['date','=', date.today().strftime(DATE_FORMAT)]])
        return request.render('opweb.opWeb_prescriptions', {'title': 'SAN-KER Pharmacy', 'pharmacyAppointments': appointments, 'pharmacyPrescriptions': prescriptions, 'medications': medications, 'services': services, 'date': date.today().strftime(DATE_FORMAT)})
    #date.today().strftime(DATE_FORMAT)

    @http.route('/opweb/stockquery', auth='public', type='json', csrf=False)
    def stockQuery(self, **post):
        quant = request.env['product.product'].sudo().search([['id','=',post['product_id']]]).qty_available
        price = request.env['product.product'].sudo().search([['id','=',post['product_id']]]).lst_price
        _logger.info(quant)
        return {'quant': quant, 'price': price}


    @http.route('/opweb/pharmacyquery', auth='public', type='json', csrf=False)
    def pharmacyPrescriptions(self, **post):
        partner_id = request.env['res.partner'].sudo().search([['id','=',post['partner_id']]])
        prescription = request.env['opweb.opweb'].sudo().search([['partner_id.id','=', post['partner_id']],['date','=', date.today().strftime(DATE_FORMAT)],['opregNo', '=', post['opreg_id']]])
        if prescription:
            med_all = []
            for line in prescription.prescription_lines:
                meds = {}
                med_name = line.med_name
                medicine = line.medicine.id
                ordered_no = line.ordered_no
                med_line_all =[]
                for det in line.medicine_lines:
                    det_array = {}
                    dose = det.dose
                    frequency = det.frequency
                    duration = det.duration
                    special = det.special
                    det_array.update({'dose':dose,'duration':duration, 'frequency':frequency, 'special':special})
                    med_line_all.append(det_array)
                meds.update({'medName': med_name, 'medicine': medicine, 'medicineQuantity':ordered_no, 'medLines': med_line_all})
                med_all.append(meds)
            service_details = []
            for s in prescription.service_lines:
                services = {}
                service_name = s.display_name
                service_charge = s.service_charge
                services.update({'serviceName': service_name, 'serviceCharge': service_charge})
                service_details.append(services)
        else:
            med_all = []
            service_details = []
        return {'name': partner_id.name, 'partner_id' : partner_id.id,'registration': partner_id.registration, 'age': partner_id.agecal, 'gender': partner_id.gender, 'prescription_lines': med_all, 'registration_charge': prescription.registration_charge, 'consultation': prescription.consultation, 'roundOff': prescription.roundOff, 'serviceDetails': service_details}

    @http.route('/opweb/sales', auth='public', type='json', csrf=False)
    def createSaleOrder(self, **post):
        presLines = []
        for line in post['params']['lines']:
            orderLine = {}
            product_id = int(line['product_id'])
            product_uom_quantity = int(line['medTotal'])
            orderLine.update({'product_id': product_id, 'product_uom_qty': product_uom_quantity})
            presLines.append((0,0, orderLine))
        for service in post['params']['services']:
            orderLine = {}
            product_id = int(service['product_id'])
            serviceCharge = float(service['serviceTotal'])
            orderLine.update({'product_id': product_id, 'price_unit': serviceCharge, 'product_uom_qty': 1})
            presLines.append((0,0, orderLine))
        createSaleVals = {
            'partner_id': post['params']['partner_id'],
            'date_order': datetime.now().strftime(DATETIME_FORMAT),
            'confirmation_date': datetime.now().strftime(DATETIME_FORMAT),
            'order_line': presLines,
            'user_id': 8,
            'warehouse_id': 4,
        }
        createSale = request.env['sale.order'].sudo().create(createSaleVals)
        createSale.action_confirm()
        Payment = request.env['account.payment'].with_context(default_invoice_ids=[(4, createSale.invoice_ids.id, False)])
        payment = Payment.create({
            'amount': post['params']['payment'],
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'partner_id': post['params']['partner_id'],
            'journal_id': 9,
            'currency_id': 20,
            'payment_date': date.today().strftime(DATE_FORMAT),
            'payment_difference_handling': 'open',
            'create_uid': 8,
            'write_uid': 8,
            'company_id':1,
            'payment_method_id': 1
        })
        payment.post() 
        opweb = request.env['opweb.opweb'].sudo().search([['date','=', date.today().strftime(DATE_FORMAT)],['opregNo', '=', post['params']['opreg_id']],['partner_id.id','=', post['params']['partner_id']]])
        opwebMedLine = []
        for line in post['params']['lines']:
            orderLine = {}
            product_id = int(line['product_id'])
            product_uom_quantity = int(line['medTotal'])
            med_name = line['med_name']
            medicine_line = []
            for each in line['lines']:
                detail = {}
                number = each['num']
                freq = each['freq']
                duration = each['duration']
                units = each['units']
                if each['special']:
                    special = each['special']
                else:
                    special = ''
                detail.update({'dose': number, 'frequency': freq, 'duration': duration, 'special': special, 'units': units})
                medicine_line.append((0,0, detail))
            orderLine.update({'medicine': product_id, 'med_name': med_name,'ordered_no': product_uom_quantity, 'medicine_lines': medicine_line})
            opwebMedLine.append((0,0, orderLine))
        opwebServiceLine = []
        roundOff = 0
        consultation = 0
        registration_charge = 0
        for det in post['params']['services']:
            if int(det['product_id']) not in [1959, 1915, 2090]:
                servicedetail = {}
                serviceId = int(det['product_id'])
                serviceCharge = float(det['serviceTotal'])
                servicedetail.update({'service': serviceId, 'service_charge': serviceCharge})
                opwebServiceLine.append((0,0, servicedetail))
            if int(det['product_id']) == 1959:
                roundOff += float(det['serviceTotal'])
            if int(det['product_id']) == 1915:
                consultation += float(det['serviceTotal'])
            if int(det['product_id']) == 2090:
                registration_charge += float(det['serviceTotal'])
        if opweb:
            for line in opweb.prescription_lines:
                line.unlink()
            for service in opweb.service_lines:
                service.unlink()
            opweb.prescription_lines = opwebMedLine
            opweb.service_lines = opwebServiceLine
            opweb.roundOff = roundOff
            opweb.consultation = consultation
            opweb.registration_charge = registration_charge
            opweb.payment = post['params']['payment']
            opweb.state = 'delivered'
        
        else:
            request.env['opweb.opweb'].sudo().create({
                'partner_id': post['params']['partner_id'],
                'date': date.today().strftime(DATE_FORMAT),
                'doctor':post['params']['doctor'],
                'prescription_lines': opwebMedLine,
                'service_lines': opwebServiceLine,
                'roundOff': roundOff,
                'consultation': consultation,
                'registration_charge': registration_charge,
                'state': 'delivered',
                'opregNo': post['params']['opreg_id'],
                'payment': post['params']['payment']
                })
        
        return 'Sale Order Generated'

    @http.route('/opweb/pharmacyupdate', auth='public', type='json', csrf=False)
    def pharmacy_update(self, **post):
        opweb = request.env['opweb.opweb'].sudo().search([['date','=', date.today().strftime(DATE_FORMAT)],['opregNo','=',post['params']['opreg_no']],['partner_id.id','=', post['params']['partner_id']]])
        opwebMedLine = []
        for line in post['params']['lines']:
            orderLine = {}
            product_id = int(line['product_id'])
            product_uom_quantity = int(line['medTotal'])
            med_name = line['med_name']
            medicine_line = []
            for each in line['lines']:
                detail = {}
                number = each['num']
                units = each['units']
                freq = each['freq']
                duration = each['duration']
                if each['special']:
                    special = each['special']
                else:
                    special = ''
                detail.update({'dose': number, 'frequency': freq, 'duration': duration, 'special': special, 'units': units})
                medicine_line.append((0,0, detail))
            orderLine.update({'medicine': product_id, 'med_name': med_name,'ordered_no': product_uom_quantity, 'medicine_lines': medicine_line})
            opwebMedLine.append((0,0, orderLine))
        opwebServiceLine = []
        roundOff = 0
        consultation = 0
        registration_charge = 0
        for det in post['params']['services']:
            if int(det['product_id']) not in [1959, 1915, 2090]:
                servicedetail = {}
                serviceId = int(det['product_id'])
                serviceCharge = float(det['serviceTotal'])
                servicedetail.update({'service': serviceId, 'service_charge': serviceCharge})
                opwebServiceLine.append((0,0, servicedetail))
                if int(det['product_id']) == 1959:
                    roundOff = float(det['serviceTotal'])
                if int(det['product_id']) == 1915:
                    consultation = float(det['serviceTotal'])
                if int(det['product_id']) == 2090:
                    registration_charge = float(det['serviceTotal'])
        if opweb:
            for line in opweb.prescription_lines:
                line.unlink()
            for service in opweb.service_lines:
                service.unlink()
            opweb.prescription_lines = opwebMedLine
            opweb.service_lines = opwebServiceLine
            opweb.roundOff = roundOff
            opweb.consultation = consultation
            opweb.registration_charge = registration_charge
            opweb.state = 'ordered'
        else:
            request.env['opweb.opweb'].sudo().create({
                'partner_id': post['params']['partner_id'],
                'date': date.today().strftime(DATE_FORMAT),
                'doctor':post['params']['doctor'],
                'prescription_lines': opwebMedLine,
                'service_lines': opwebServiceLine,
                'roundOff': roundOff,
                'consultation': consultation,
                'registration_charge': registration_charge,
                'opregNo': post['params']['opreg_no'],
                'state': 'ordered'
                })
        return 'Prescription Updated'

    @http.route('/opweb/printquery', auth='public', type='json', csrf=False)
    def printquery(self, **post):
        reportid = int(post['report_id'])
        _logger.info(reportid)
        opwebId = request.env['opweb.opweb'].sudo().search([['opregNo','=', reportid]])
        return opwebId.id
