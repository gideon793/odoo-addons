odoo.define('opweb.opnewrow', function (require) {
    "use strict";
    $(document).ready(function () {
        $(document).on('keyup', '#navSearch', function () {
            let input = document.getElementById('navSearch').value;
            input = input.toLowerCase();
            let patListToday = document.getElementsByClassName('apptListItem');
            for (i = 0; i < patListToday.length; i++) {
                if (!patListToday[i].innerHTML.toLowerCase().includes(input)) {
                    patListToday[i].style.display = "none";
                    patListToday[i].closest('.pharmacyLi').style.display = "none";
                }
                else {
                    patListToday[i].style.display = "list-item";
                    patListToday[i].closest('.pharmacyLi').style.display = "list-item";

                }
            }
        });
        function pharmacyServicesUpdate(serviceUpdate){
            document.getElementById('registrationCharge').value = serviceUpdate['registration_charge'];
            document.getElementById('registrationCharge').dispatchEvent(new Event('change', { bubbles: true }));
            document.getElementById('roundOff').value = serviceUpdate['roundOff'];
            document.getElementById('roundOff').dispatchEvent(new Event('change', { bubbles: true }));
            document.getElementById('consultationCharge').value = serviceUpdate['consultationCharge'];
            document.getElementById('consultationCharge').dispatchEvent(new Event('change', { bubbles: true }));
            var serviceLineEntries = document.getElementById('servicesContainer').getElementsByClassName('serviceAdditional');
            for (var i=serviceLineEntries.length -1; i>=0; --i){
                serviceLineEntries[i].remove();
            }
            for (var i= 0; i<serviceUpdate['serviceLines'].length; i++){
                var div = document.createElement('div');
                div.innerHTML = document.getElementById('servicesEntries').innerHTML;
                div.classList.add('serviceAdditional');
                div.getElementsByClassName('serviceName')[0].value = serviceUpdate['serviceLines'][i]['serviceName'];
                div.getElementsByClassName('serviceCharge')[0].value = serviceUpdate['serviceLines'][i]['serviceCharge'];                
                div.getElementsByClassName('serviceCharge')[0].dispatchEvent(new Event('change', { bubbles: true }));
                document.getElementById('servicesContainer').appendChild(div);    
            };
            
        }
        function pharmacyDemographics(opPrescription) {
            document.getElementById('patName').innerHTML = opPrescription['name'];
            document.getElementById('patName').doctor = opPrescription['doctor'];
            document.getElementById('patAge').innerHTML = opPrescription['age'] + '/' + opPrescription['gender'];
            document.getElementById('patReg').innerHTML = opPrescription['registration'];
            document.getElementById('patName').partner_id = opPrescription['partner_id'];
            document.getElementById('patName').opregID = opPrescription['opreg_id'];
            var doctorDict = {  'ssyiem': 'Dr. S. Syiem', 
                            'eddie': 'Dr. E. Mukhim',
                            'didak': 'Dr. D. Khonglah',
                            'gideon': 'Dr. G. Rynjah', 
                            'rlaloo':  'Dr. R. Laloo',
                            'lashngain': 'Dr.  L. Sohliya', 
                            'dkynjin': 'Dr. D. Kynjin',}
            document.getElementById('apptDoctor').innerHTML = doctorDict[opPrescription['doctor']];

        }

        function updatePrescription(passPres) {
            var mainPrescription = document.getElementById('presMain');
            var presLines = mainPrescription.getElementsByClassName('presLine');
            for (var le = presLines.length - 1; le >= 0; --le) {
                presLines[le].remove();
            };
            for (var tp = 0; tp < passPres.length; tp++) {
                var div = document.createElement('div');
                div.innerHTML = document.getElementById('prescriptionLine').innerHTML;
                div.getElementsByClassName('presMedName')[0].value = passPres[tp].medName;
                if (passPres[tp].medicine) {
                    div.getElementsByClassName('presMedName')[0].dataset.product_id = passPres[tp].medicine;
                } else {
                    div.getElementsByClassName('presMedName')[0].dataset.product_id = '';
                }
                div.getElementsByClassName('medTotal')[0].value = passPres[tp].medicineQuantity;
                if (passPres[tp].medLines.length >0 ) {
                    div.getElementsByClassName('medicineRowContainer')[0].getElementsByClassName('medicineLines')[0].remove();
                    for (var tpl = 0; tpl < passPres[tp].medLines.length; tpl++) {
                        var presLineHtml = document.createElement('div');
                        presLineHtml.innerHTML = document.getElementById('medDetailEntry').innerHTML;
                        presLineHtml.getElementsByClassName('med_no')[0].value = passPres[tp].medLines[tpl].dose;
                        presLineHtml.getElementsByClassName('med_freq')[0].value = passPres[tp].medLines[tpl].frequency;
                        presLineHtml.getElementsByClassName('med_duration')[0].value = passPres[tp].medLines[tpl].duration;
                        if (passPres[tp].medLines[tpl].special) {
                            presLineHtml.getElementsByClassName('med_special')[0].value = passPres[tp].medLines[tpl].special;
                        }
                        div.getElementsByClassName('medicineRowContainer')[0].appendChild(presLineHtml);
                    }
                } else {
                    div.getElementsByClassName('medicineRowContainer')[0].getElementsByClassName('medicineLines')[0].remove();
                    var presLineHtml = document.createElement('div');
                    presLineHtml.innerHTML = document.getElementById('medDetailEntry').innerHTML;
                    div.getElementsByClassName('medicineRowContainer')[0].appendChild(presLineHtml);
                }
                console.log(div);
                mainPrescription.appendChild(div);
            }
            var meds = mainPrescription.getElementsByClassName('medTotal');
            for (var i = 0; i < meds.length; i++) {
                meds[i].dispatchEvent(new Event('change', { bubbles: true }));
            }

        }
        function oldPrescriptionUpdate(oldPres, pat_id) {
            var old_pres = document.getElementById('old_prescriptions');
            old_pres.innerHTML = '';
            var ulElement = document.createElement('ul');
            ulElement.classList.add('pres_list');
            for (var i = 0; i < oldPres.length; i++) {
                var date_inside = new Date(oldPres[i]['date']).toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });
                var liNew = document.createElement('li');
                liNew.classList.add('pl-0', 'pt-1', 'mt-1', 'card_pat', 'shadow', 'rounded');
                var aNew = document.createElement('a');
                aNew.href = '#';
                aNew.classList.add('old_pres_det')
                aNew.dataset.date_inside = date_inside;
                aNew.dataset.pat_id = pat_id;
                aNew.dataset.id = i;
                aNew.pres = oldPres[i]['medLines'];
                aNew.presDetail = oldPres[i];
                aNew.innerHTML = date_inside;
                liNew.appendChild(aNew);
                ulElement.appendChild(liNew);
            }
            old_pres.appendChild(ulElement);
        }
        if (document.getElementById('pat_no_list')) {
            document.getElementById('pat_no_list').innerHTML = pat_list.length;
            var today_list = document.getElementById('opd_list');
            var pat_list_html = '<ul class="appt_sidebar">';
            for (var i = 0; i < pat_list.length; i++) {
                if (pat_list[i][5] == 'new') {
                    var appt_type = 'N';
                }
                else if (pat_list[i][5] == 'old') {
                    var appt_type = 'O';
                }
                else {
                    var appt_type = 'M';
                };
                pat_list_html = pat_list_html + '<li class="card_pat shadow"><a href="#" class="patient_click" id="pat[' + i + ']"><i class="p-1 fa fa-prescription"></i>' + pat_list[i][0] + '<span class="badge badge-primary ml-1">' + appt_type + '</span><br />' + pat_list[i][2] + '</li></a>';
            };
            pat_list_html = pat_list_html + '</ul>';
            today_list.innerHTML = pat_list_html;
        };
        $(document).on('click', '.repeat_btn', function () {
            var tr = $(this).closest('tr').parent().closest('tr').index();
            var row_search = tr + '_medication_details';
            var table = document.getElementById(row_search).children[0];
            var row = table.insertRow(-1);
            row.innerHTML = document.getElementById(tr + '_medication_details_row_' + row.rowIndex).innerHTML;
            row.id = tr + '_medication_details_row_' + (row.rowIndex + 1);
            row.cells[0].children[0].children[0].children[0].id = tr + '_medNo_' + (row.rowIndex + 1);
        });

        $(document).on('click', '.patient_click', function () {
            var pat_id = this.id.substring(4, this.id.length - 1);
            console.log($(this));
            var pat_enquiry = {};
            var oldPrescriptionList = [];
            pat_enquiry['params'] = { 'partner_id': pat_list[pat_id][1], 'date': date, 'opregId': Number(pat_list[pat_id][7])};
            var pat_enquiry_json = JSON.stringify(pat_enquiry);
            function serverCall() {
                return $.ajax({
                    type: "POST",
                    datatype: "json",
                    contentType: 'application/json',
                    url: "http://192.168.2.100:8069/opweb/patdetail",
                    data: pat_enquiry_json,
                    success: function (data) {
                        console.log(data)
                    }
                });
            }
            $.when(serverCall()).done(function (a1) {
                var todayPrescription = a1['result']['prescription_lines'];
                oldPrescriptionList = a1['result']['old_prescriptions'];
                updatePrescription(todayPrescription);
                oldPrescriptionUpdate(oldPrescriptionList, pat_id);
            });
            var str = pat_list[pat_id][0];
            document.getElementById('patient_name').innerHTML = str;
            document.getElementById('form_pat_id').innerHTML = pat_list[pat_id][1];
            document.getElementById('form_pat_id').opregID = Number(pat_list[pat_id][7]);
            var diagnosis_display = [];
            var dd = 0;
            while (dd < pat_list[pat_id][6].length) {
                diagnosis_display.push(pat_list[pat_id][6][dd]);
                dd += 1;
            };
            document.getElementById('diagnosis').innerHTML = diagnosis_display;
            var pat_det_list = document.getElementById('patient_details');
            pat_det_list.innerHTML = pat_list[pat_id][2];
            document.getElementById('patient_age').innerHTML = pat_list[pat_id][3] + '/' + pat_list[pat_id][4];
        });

        $(document).on('click', '.old_pres_det', function () {
            var date_inside = $(this).data('date_inside');
            var pres_id = $(this).data('id');
            document.getElementById('pres_date').innerHTML = date_inside;
            var pres_details = $(this)[0].pres;
            var oldPresDetails = document.getElementById('oldPrescriptionDetail');
            oldPresDetails.innerHTML = '';
            oldPresDetails.presDetail = $(this)[0].pres;
            for (i = 0; i < pres_details.length; i++) {
                var oldPrescriptionLines = document.createElement('div');
                oldPrescriptionLines.classList.add('oldPrescriptionLines', 'row');
                var oldPres1 = document.createElement('div');
                oldPres1.classList.add('col-1')
                oldPres1.innerHTML = i + 1;
                var oldPres2 = document.createElement('div');
                oldPres2.classList.add('col-5');
                oldPres2.innerHTML = pres_details[i]['medName'];
                var oldPres8 = document.createElement('div');
                oldPres8.classList.add('col-1');
                oldPres8.innerHTML = pres_details[i]['medicineQuantity'];
                var oldPres3 = document.createElement('div');
                oldPres3.classList.add('col-1');
                var oldPres4 = document.createElement('div');
                oldPres4.classList.add('col-1');
                var oldPres5 = document.createElement('div');
                oldPres5.classList.add('col-1');
                var oldPres6 = document.createElement('div');
                oldPres6.classList.add('col-1')
                var oldPres7 = document.createElement('div');
                oldPres7.classList.add('col-1')
                var freqValues = { '1': 'OD', '2': 'BD', '3': 'TID', '4': 'PID', '5': 'PID', '6': 'HSOD', '7': 'SOS', '8': 'stat', '9':'others' }
                if (pres_details[i]['medicineLines']) {
                    for (var pd = 0; pd < pres_details[i]['medicineLines'].length; pd++) {
                        var oldPres3add = '';
                        oldPres3add = document.createElement('div');
                        oldPres3add.classList.add('presLineOld')
                        oldPres3add.innerHTML = pres_details[i]['medicineLines'][pd]['dose'];
                        oldPres3.appendChild(oldPres3add);
                        var oldPres4add = '';
                        oldPres4add = document.createElement('div');
                        oldPres4add.classList.add('presLineOld');
                        oldPres4add.innerHTML = pres_details[i]['medicineLines'][pd]['units']
                        oldPres4.appendChild(oldPres4add);
                        var oldPres5add = '';
                        oldPres5add = document.createElement('div');
                        oldPres5add.classList.add('presLineOld')
                        oldPres5add.innerHTML = freqValues[pres_details[i]['medicineLines'][pd]['frequency']];
                        oldPres5.appendChild(oldPres5add);
                        var oldPres6add = '';
                        oldPres6add = document.createElement('div');
                        oldPres6add.classList.add('presLineOld');
                        oldPres6add.innerHTML = pres_details[i]['medicineLines'][pd]['duration'];
                        oldPres6.appendChild(oldPres6add);
                        var oldPres7add = '';
                        oldPres7add.classList.add('presLineOld');
                        if (pres_details[i]['medicineLines'][pd]['special']) {
                            oldPres7add.innerHTML = pres_details[i]['medicineLines'][pd]['special'];
                        } else {
                            oldPres7add.innerHTML = "-";
                        };
                        oldPres7.appendChild(oldPres7add)

                    }
                }
                else {
                    oldPres3.innerHTML = '-';
                    oldPres4.innerHTML = '-';
                    oldPres5.innerHTML = '-';
                    oldPres6.innerHTML = '-';
                    oldPres7.innerHTML = '-';
                };
                oldPrescriptionLines.append(oldPres1, oldPres2, oldPres3, oldPres4, oldPres5, oldPres6, oldPres7, oldPres8);
                oldPresDetails.appendChild(oldPrescriptionLines);
            };
            $('#old_prescript_modal').modal('show');
        });

        $(document).on('click', '.pres_submit', function () {
            updatePrescription(document.getElementById('oldPrescriptionDetail').presDetail);
            $('#old_prescript_modal').modal('hide');
        });
        $('#opnewrow').click(function (e) {
            var div = document.createElement('div');
            div.innerHTML = document.getElementById('prescriptionLine').innerHTML;
            document.getElementById('presMain').appendChild(div);
        });
        $(document).on('click', '.faPlus', function () {
            var div = document.createElement('div');
            div.innerHTML = document.getElementById('medDetailEntry').innerHTML;
            $(this).closest('.medicineRowContainer')[0].appendChild(div);

        });
        $(document).on('click', '.delMed', function () {
            $(this).closest('.presLine').remove();

        });
        $(document).on('click', '.faMinus', function () {
            var faMinusIndex = $($(this).closest('.medicineRowContainer')[0].getElementsByClassName('medicineLines')).index($(this).closest('.medicineLines'));
            if (faMinusIndex != 0) {
                $(this).closest('.medicineLines').remove();
            }
        });
        $('#old_pres_listCollapse').on('click', function () {
            $('#old_pres_list').toggleClass('active');
        });
        $('#preslistCollapse').on('click', function (){
            $('#oldPreslist').toggleClass('active');
        })
        $(document).on('change', '.med_duration, .med_no, .med_freq', function () {
            var medTotalOrder = 0;
            var presTotalLines = $(this).closest('.presLineDetails')[0].getElementsByClassName('medicineLines');
            for (var t = 0; t < presTotalLines.length; t++) {
                var med_quant = Number(presTotalLines[t].getElementsByClassName('med_no')[0].value);
                var med_frequency = Number(presTotalLines[t].getElementsByClassName('med_freq')[0].value);
                var med_duration = Number(presTotalLines[t].getElementsByClassName('med_duration')[0].value);
                var lineTotal = med_quant * med_frequency * med_duration;
                medTotalOrder += lineTotal;
            }
            $(this).closest('.presLineDetails')[0].getElementsByClassName('medTotal')[0].value = medTotalOrder;
        });
        $('#form_submit').click(function (e) {
            if (confirm('Submit Prescription?')){
            var san_form = {};
            var form_pat = document.getElementById('form_pat_id').innerHTML;
            var formOPregID = document.getElementById('form_pat_id').opregID;
            var presDetails = [];
            var mainPrescription = document.getElementById('presMain').getElementsByClassName('presLine');
            for (var mD = 0; mD < mainPrescription.length; mD++) {
                var medDetails = {};
                var medName = mainPrescription[mD].getElementsByClassName('presMedName')[0].value;
                const result = med_details.find(({ med_name }) => med_name === medName);
                if (result) {
                    medDetails.med_id = result.med_id;
                    medDetails.name = result.med_name;
                } else {
                    medDetails.med_id = '';
                    medDetails.name = medName;
                }
                var medTotal = mainPrescription[mD].getElementsByClassName('medTotal')[0].value;
                medDetails.medTotal = medTotal;
                var presMedDetails = mainPrescription[mD].getElementsByClassName('medicineRowContainer')[0].getElementsByClassName('medicineLines');
                var presLines = [];
                for (var mpl = 0; mpl < presMedDetails.length; mpl++) {
                    var presLineEntries = {};
                    presLineEntries.num = presMedDetails[mpl].getElementsByClassName('med_no')[0].value;
                    presLineEntries.freq = presMedDetails[mpl].getElementsByClassName('med_freq')[0].value;
                    presLineEntries.duration = presMedDetails[mpl].getElementsByClassName('med_duration')[0].value;
                    presLineEntries.special = presMedDetails[mpl].getElementsByClassName('med_special')[0].value;
                    presLineEntries.units = presMedDetails[mpl].getElementsByClassName('medUnits')[0].value;
                    presLines.push(presLineEntries);
                }
                medDetails.lines = presLines;
                presDetails.push(medDetails)
            }
            san_form['params'] = { 'partner_id': form_pat, 'doctor': doctor, 'date': date, 'prescription': presDetails, 'opreg_id': formOPregID }
            var san_form_json = JSON.stringify(san_form);
            console.log(san_form_json);
            $.ajax({
                type: "POST",
                datatype: "json",
                contentType: 'application/json',
                url: "http://192.168.2.100:8069/opweb/prescription",
                data: san_form_json,
                success: function (data) {
                    alert(data['result']);
                }
            })
        }
        });
        if (document.getElementById('navMain')) {
            var list = document.getElementById('pharmacyNavbar');
            var pharmacyMainul = document.createElement('ul');
            pharmacyMainul.classList.add('pharmacyList', 'list-unstyled');
            for (var l = 0; l < todayPharmacyPrescriptions.length; l++) {
                var pharmacyLi = document.createElement('li');
                pharmacyLi.classList.add('pharmacyLi');
                var liPatient = document.createElement('a');
                liPatient.href = "#"
                liPatient.classList.add('apptListItem');
                liPatient.innerHTML = todayPharmacyPrescriptions[l]['name'];
                liPatient.dataset['partner_id'] = todayPharmacyPrescriptions[l]['partner_id']
                liPatient.dataset['doctor'] = todayPharmacyPrescriptions[l]['doctor']
                liPatient.dataset['opreg_id'] = todayPharmacyPrescriptions[l]['opreg_id']
                let obj = todayOpwebPrescriptions.find(o => o.name === todayPharmacyPrescriptions[l]['name']);
                if (obj) {
                    if (obj.state == 'delivered'){
                        var presBadge = document.createElement('span');
                        presBadge.classList.add('badge', 'badge-danger');
                        var starIcon = document.createElement('i');
                        starIcon.classList.add('fa', 'fa-star');
                        presBadge.append(starIcon);
                        liPatient.append(presBadge);
                        pharmacyLi.dataset['state'] = obj.state;
                    }
                    else{
                        var presBadge = document.createElement('span');
                        presBadge.classList.add('badge', 'badge-success');
                        var starIcon = document.createElement('i');
                        starIcon.classList.add('fa', 'fa-star');
                        presBadge.append(starIcon);
                        liPatient.append(presBadge);
                        pharmacyLi.dataset['state'] = obj.state;

                    }
                }
                else {
                    pharmacyLi.dataset['state'] = 'draft';
                };
                pharmacyLi.appendChild(liPatient);
                pharmacyMainul.appendChild(pharmacyLi);
            }
            var sortedUlist = document.createElement('ul');
            sortedUlist.classList.add('pharmacyList', 'list-unstyled');
            var items = pharmacyMainul.querySelectorAll('li');
            for (var j = 0, array = ['ordered', 'draft' , 'delivered' ]; j < array.length; j++) {
                for (var i = 0; i < items.length; i++) {
                    if (items[i].dataset['state'] === array[j]) {
                        sortedUlist.appendChild(items[i]);
                    };
                }
            };
            list.appendChild(sortedUlist);
        };
        $(document).on('click', '.apptListItem', function () {
            var partnerId = {};
            var partnerIdThis = $(this)[0].dataset['partner_id']
            partnerId['params'] = { 'partner_id': $(this)[0].dataset['partner_id'], 'opreg_id':  $(this)[0].dataset['opreg_id']};
            var pharmacyJSON = JSON.stringify(partnerId);
            var prescriptionDoctor = $(this)[0].dataset['doctor'];
            var prescriptionOPregID = $(this)[0].dataset['opreg_id'];
            console.log(pharmacyJSON);
            function pharmacyserverCall() {
                return $.ajax({
                    type: "POST",
                    datatype: "json",
                    contentType: 'application/json',
                    url: "http://192.168.2.100:8069/opweb/pharmacyquery",
                    data: pharmacyJSON,
                    success: function (data) {
                    }
                });
            };
            $.when(pharmacyserverCall()).done(function (a1) {
                var results = a1['result']
                var todayPrescription = results['prescription_lines'];
                var serviceDetails = {'consultationCharge': results['consultation'], 'roundOff': results['roundOff'], 'registration_charge': results['registration_charge'], 'serviceLines': results['serviceDetails']}
                var prescriptionDemographics = { 'name': results['name'], 'registration': results['registration'], 'age': results['age'], 'gender': results['gender'], 'partner_id': results['partner_id'], 'doctor': prescriptionDoctor, 'opreg_id': prescriptionOPregID };
                updatePrescription(todayPrescription);
                pharmacyDemographics(prescriptionDemographics);
                pharmacyServicesUpdate(serviceDetails);
                var patientdetailJSON = JSON.stringify({'params': {'partner_id': partnerIdThis, 'date': date, 'opregId': Number(prescriptionOPregID)}})
                console.log(patientdetailJSON);
                function patientdetail(){
                    return $.ajax({
                        type: "POST",
                        datatype: "json",
                        contentType: 'application/json',
                        url: "http://192.168.2.100:8069/opweb/patdetail",
                        data: patientdetailJSON,
                        success: function (data) {
                            console.log(data);
                        }
                    });
                };
                $.when(patientdetail()).done(function (a1){
                    var oldPrescriptionList = a1['result']['old_prescriptions']
                    oldPrescriptionUpdate(oldPrescriptionList, partnerIdThis);
                    document.getElementById('paymentTotal').value = a1['result']['payment'];

                });                
            });
        });
        $('#pharmacyDetails').unbind().on('change', '.medTotal', function () {
            var selectedMed = $(this)[0].parentElement.children[1].value;
            var productClick = $(this)[0];
            var productPrice = productClick.parentElement.children[2].querySelector('option[value="' + selectedMed + '"]').getAttribute('med_price');
            var productIdQuery = $(this)[0].parentElement.children[2].querySelector('option[value="' + selectedMed + '"]').id;
            if (productIdQuery) {
                var productId = JSON.stringify({ 'params': { 'product_id': productIdQuery } });
                function medGetStock() {
                    return $.ajax({
                        type: 'POST',
                        datatype: 'json',
                        contentType: 'application/json',
                        url: "http://192.168.2.100:8069/opweb/stockquery",
                        data: productId,
                    });
                };
                $.when(medGetStock()).done(function (a1) {
                    var totalOrder = productClick.value;
                    var availability = a1['result']['quant'] - totalOrder;
                    var stockPrint = document.createElement('span');
                    if (availability < 0) {
                        stockPrint.classList.add('badge', 'badge-danger', 'avail');
                    } else {
                        stockPrint.classList.add('badge', 'badge-success', 'avail');
                    }
                    stockPrint.innerHTML = availability;
                    var oldAvail = productClick.parentElement.getElementsByClassName('avail');
                    for (var i = oldAvail.length - 1; i >= 0; --i) {
                        oldAvail[i].remove();
                    };
                    ;
                    var lineTotal = productClick.parentElement.parentElement.getElementsByClassName('lineTotal');
                    var thisTotal = (totalOrder * Number(productPrice));
                    lineTotal[0].innerText = thisTotal.toFixed(2);
                    lineTotal[0].value = thisTotal.toFixed(2);
                    lineTotal[0].dataset.line_total = thisTotal.toFixed(2);
                    productClick.parentElement.appendChild(stockPrint);
                });
            };
        });
        $('#pharmacyFormSubmit').click(function (e) {
            if (confirm('Confirm Sale Order?')){
            var params = {};
            var formPat = document.getElementById('patName').partner_id;
            var formDoctor = document.getElementById('patName').doctor;
            var formOPregID = document.getElementById('patName').opregID;
            var paymentDetail = document.getElementById('paymentTotal').value;
            var presDetails = [];
            var mainPrescription = document.getElementById('presMain').getElementsByClassName('presLine');
            for (var mD = 0; mD < mainPrescription.length; mD++) {
                var medDetails = {};                
                var medName = mainPrescription[mD].getElementsByClassName('presMedName')[0].value;
                var productId = mainPrescription[mD].querySelector('option[value="' + medName + '"]').id;
                var medPrice = mainPrescription[mD].querySelector('option[value="' + medName + '"]').med_price;                
                if (productId) {
                    var medTotal = mainPrescription[mD].getElementsByClassName('medTotal')[0].value;
                    medDetails.product_id = productId;
                    medDetails.med_name = medName;
                    medDetails.medTotal = medTotal;
                    var presMedDetails = mainPrescription[mD].getElementsByClassName('medicineRowContainer')[0].getElementsByClassName('medicineLines');
                    var presLines = [];
                    for (var mpl = 0; mpl < presMedDetails.length; mpl++) {
                        var presLineEntries = {};
                        presLineEntries.num = presMedDetails[mpl].getElementsByClassName('med_no')[0].value;
                        presLineEntries.freq = presMedDetails[mpl].getElementsByClassName('med_freq')[0].value;
                        presLineEntries.duration = presMedDetails[mpl].getElementsByClassName('med_duration')[0].value;
                        presLineEntries.special = presMedDetails[mpl].getElementsByClassName('med_special')[0].value;
                        presLineEntries.units = presMedDetails[mpl].getElementsByClassName('medUnits')[0].value;
                        presLines.push(presLineEntries);
                    }
                    medDetails.lines = presLines;
                    presDetails.push(medDetails);
        
                }
                else{
                    var medTotal = mainPrescription[mD].getElementsByClassName('medTotal')[0].value;
                    medDetails.product_id = '';
                    medDetails.med_name = medName;
                    medDetails.medTotal = medTotal;
                    var presMedDetails = mainPrescription[mD].getElementsByClassName('medicineRowContainer')[0].getElementsByClassName('medicineLines');
                    var presLines = [];
                    for (var mpl = 0; mpl < presMedDetails.length; mpl++) {
                        var presLineEntries = {};
                        presLineEntries.num = presMedDetails[mpl].getElementsByClassName('med_no')[0].value;
                        presLineEntries.freq = presMedDetails[mpl].getElementsByClassName('med_freq')[0].value;
                        presLineEntries.duration = presMedDetails[mpl].getElementsByClassName('med_duration')[0].value;
                        presLineEntries.special = presMedDetails[mpl].getElementsByClassName('med_special')[0].value;
                        presLineEntries.units = presMedDetails[mpl].getElementsByClassName('medUnits')[0].value;
                        presLines.push(presLineEntries);
                    }
                    medDetails.lines = presLines;
                    presDetails.push(medDetails);
                };
            };
            var servicesLines = [];
            var mainServices = document.getElementById('servicesContainer').getElementsByClassName('serviceDetail');
            servicesLines.push({ 'product_id': '1959', 'serviceTotal': document.getElementById('roundOff').value }, { 'product_id': '1915', 'serviceTotal': document.getElementById('consultationCharge').value }, { 'product_id': '2090', 'serviceTotal': document.getElementById('registrationCharge').value })
            for (var g = 0; g < mainServices.length; g++) {
                var serviceDetail = {}
                var serviceName = mainServices[g].getElementsByClassName('serviceName')[0].value;
                var serviceId = mainServices[g].querySelector('option[value="' + serviceName + '"]').getAttribute('product_id');
                serviceDetail.product_id = serviceId;
                serviceDetail.serviceTotal = mainServices[g].getElementsByClassName('serviceCharge')[0].value;
                servicesLines.push(serviceDetail);
            }
            params.services = servicesLines;
            params.partner_id = formPat;
            params.lines = presDetails;
            params.payment = paymentDetail;
            params.doctor = formDoctor;
            params.opreg_id = formOPregID;
            var saleOrderJSON = JSON.stringify({ 'params': { params } });
            console.log(saleOrderJSON);
            $.ajax({
                type: "POST",
                datatype: "json",
                contentType: 'application/json',
                url: "http://192.168.2.100:8069/opweb/sales",
                data: saleOrderJSON,
                success: function (data) {
                    alert(data['result']);
                }
            })
        }
        });
        $('#serviceNewRow').click(function (e) {
            var div = document.createElement('div');
            div.innerHTML = document.getElementById('servicesEntries').innerHTML;
            div.classList.add('serviceAdditional');
            document.getElementById('servicesContainer').appendChild(div);
        });
        $(document).on('click','.delService',function(e){
            $(this).closest('.serviceAdditional').remove();
        })
        $('#pharmacyMain').on('change', '.consultationCharge, .registrationCharge, .medTotal, .serviceCharge, .roundOff', function(){
            var presTotal = 0;
            var presLine = document.getElementById('presMain').getElementsByClassName('mainMed');
            for (var i=0; i<presLine.length; i++){
                var selectedLine = presLine[i].getElementsByClassName('presMedName')[0].value;
                var linePrice = presLine[i].querySelector('option[value="' + selectedLine + '"]').getAttribute('med_price');
                presTotal+= Number(linePrice) * presLine[i].getElementsByClassName('medTotal')[0].value;
            }
            var serviceLineTotal = document.getElementById('servicesMain').getElementsByClassName('serviceCharge');
            for (var i=0; i<serviceLineTotal.length; i++){
                presTotal += Number(serviceLineTotal[i].value);
            }
            presTotal += Number(document.getElementById('consultationCharge').value);
            presTotal += Number(document.getElementById('registrationCharge').value);
            presTotal += Number(document.getElementById('roundOff').value);
            document.getElementById('amountTotal').innerText = presTotal.toFixed(2);
        });
        $('#pharmacyUpdateSubmit').click(function(e){
            var params = {};
            var formPat = document.getElementById('patName').partner_id;
            var formopregID = document.getElementById('patName').opregID;
            var formDoctor = document.getElementById('patName').doctor;
            var paymentDetail = document.getElementById('paymentTotal').value;
            var presDetails = [];
            var mainPrescription = document.getElementById('presMain').getElementsByClassName('presLine');
            for (var mD = 0; mD < mainPrescription.length; mD++) {
                var medDetails = {};                
                var medName = mainPrescription[mD].getElementsByClassName('presMedName')[0].value;
                var productId = mainPrescription[mD].querySelector('option[value="' + medName + '"]').id;
                var medPrice = mainPrescription[mD].querySelector('option[value="' + medName + '"]').med_price;                
                if (productId) {
                    var medTotal = mainPrescription[mD].getElementsByClassName('medTotal')[0].value;
                    medDetails.product_id = productId;
                    medDetails.med_name = medName;
                    medDetails.medTotal = medTotal;
                    var presMedDetails = mainPrescription[mD].getElementsByClassName('medicineRowContainer')[0].getElementsByClassName('medicineLines');
                    var presLines = [];
                    for (var mpl = 0; mpl < presMedDetails.length; mpl++) {
                        var presLineEntries = {};
                        presLineEntries.num = presMedDetails[mpl].getElementsByClassName('med_no')[0].value;
                        presLineEntries.freq = presMedDetails[mpl].getElementsByClassName('med_freq')[0].value;
                        presLineEntries.duration = presMedDetails[mpl].getElementsByClassName('med_duration')[0].value;
                        presLineEntries.special = presMedDetails[mpl].getElementsByClassName('med_special')[0].value;
                        presLineEntries.units = presMedDetails[mpl].getElementsByClassName('medUnits')[0].value;
                        presLines.push(presLineEntries);
                    }
                    medDetails.lines = presLines;
                    presDetails.push(medDetails);
        
                }
                else{
                    var medTotal = mainPrescription[mD].getElementsByClassName('medTotal')[0].value;
                    medDetails.product_id = '';
                    medDetails.med_name = medName;
                    medDetails.medTotal = medTotal;
                    var presMedDetails = mainPrescription[mD].getElementsByClassName('medicineRowContainer')[0].getElementsByClassName('medicineLines');
                    var presLines = [];
                    for (var mpl = 0; mpl < presMedDetails.length; mpl++) {
                        var presLineEntries = {};
                        presLineEntries.num = presMedDetails[mpl].getElementsByClassName('med_no')[0].value;
                        presLineEntries.freq = presMedDetails[mpl].getElementsByClassName('med_freq')[0].value;
                        presLineEntries.units = presMedDetails[mpl].getElementsByClassName('medUnits')[0].value;
                        presLineEntries.duration = presMedDetails[mpl].getElementsByClassName('med_duration')[0].value;
                        presLineEntries.special = presMedDetails[mpl].getElementsByClassName('med_special')[0].value;
                        presLines.push(presLineEntries);
                    }
                    medDetails.lines = presLines;
                    presDetails.push(medDetails);
                };
            };
            var servicesLines = [];
            var mainServices = document.getElementById('servicesContainer').getElementsByClassName('serviceDetail');
            servicesLines.push({ 'product_id': '1959', 'serviceTotal': document.getElementById('roundOff').value }, { 'product_id': '1915', 'serviceTotal': document.getElementById('consultationCharge').value }, { 'product_id': '2090', 'serviceTotal': document.getElementById('registrationCharge').value })
            for (var g = 0; g < mainServices.length; g++) {
                var serviceDetail = {}
                var serviceName = mainServices[g].getElementsByClassName('serviceName')[0].value;
                var serviceId = mainServices[g].querySelector('option[value="' + serviceName + '"]').getAttribute('product_id');
                serviceDetail.product_id = serviceId;
                serviceDetail.serviceTotal = mainServices[g].getElementsByClassName('serviceCharge')[0].value;
                servicesLines.push(serviceDetail);
            }
            params.services = servicesLines;
            params.partner_id = formPat;
            params.lines = presDetails;
            params.opreg_no = formopregID;
            params.payment = paymentDetail;
            params.doctor = formDoctor;
            var saleOrderJSON = JSON.stringify({ 'params': { params } });
            $.ajax({
                type: "POST",
                datatype: "json",
                contentType: 'application/json',
                url: "http://192.168.2.100:8069/opweb/pharmacyupdate",
                data: saleOrderJSON,
                success: function (data) {
                    alert(data['result']);
                }
            })
        });
        $('#printPrescription').click(function(e){
            var opwebID;
            function printPrescription(){
            return $.ajax({
                    type: "POST",
                    datatype: "json",
                    contentType: 'application/json',
                    url: "http://192.168.2.100:8069/opweb/printquery",
                    data: JSON.stringify({'params': {'report_id': document.getElementById('patName').opregID}}),
                    success: function (data) {
                    }
                });
            };
            $.when(printPrescription()).done(function (a1){
                console.log(a1);
                var reportURL = 'http://192.168.2.100:8069/report/pdf/opweb.opdPrescription_template/' + a1['result'];
                window.open(reportURL).print();
            });
        });
        $('#printReceipt').click(function(e){
            var xmlReceipt = document.implementation.createDocument(null, "receipt");
            var receipt = xmlReceipt.getElementsByTagName('receipt')[0];
            var header = xmlReceipt.createElement('h2');
            header.innerHTML = 'SAN-KER';
            header.setAttribute('align', 'center');
            receipt.appendChild(header);
            var br = xmlReceipt.createElement('br');
            receipt.appendChild(br);
            var title = xmlReceipt.createElement('h4');
            title.innerHTML = 'Pharmacy Bill';
            title.setAttribute('align', 'center');
            receipt.appendChild(title);
            var br = xmlReceipt.createElement('br');
            receipt.appendChild(br);
            var br = xmlReceipt.createElement('br');
            receipt.appendChild(br);
            var xmlPatName = xmlReceipt.createElement('h3');
            xmlPatName.setAttribute('align', 'left');
            xmlPatName.innerHTML = 'Name:' + String(document.getElementById('patName').innerHTML);
            receipt.appendChild(xmlPatName);
            var xmlRegNo = xmlReceipt.createElement('span');
            xmlRegNo.setAttribute('align', 'left');
            xmlRegNo.innerHTML = 'Registration: '+ String(document.getElementById('patReg').innerHTML);
            receipt.appendChild(xmlRegNo);
            var xmlDate = xmlReceipt.createElement('span');
            var receiptDate = new Date(date).toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });
            xmlDate.setAttribute('align', 'left');
             xmlDate.innerHTML = 'Date: ' + receiptDate;
            receipt.appendChild(xmlDate);
            var br = xmlReceipt.createElement('br');
            receipt.appendChild(br);
            var hr = xmlReceipt.createElement('span');
            hr.setAttribute('align', 'center');
            hr.innerHTML = '------------------------------';
            receipt.appendChild(hr);
            var br = xmlReceipt.createElement('br');
            receipt.appendChild(br);
            var mainPrescription = document.getElementById('presMain').getElementsByClassName('presLine');
            for (var i = 0; i < mainPrescription.length; i++){
                var medName = mainPrescription[i].getElementsByClassName('presMedName')[0].value;
                var productId = mainPrescription[i].querySelector('option[value="' + medName + '"]').id;
                var medPrice = Number(mainPrescription[i].querySelector('option[value="' + medName + '"]').getAttribute('med_price')).toFixed(2);
                console.log(productId, medPrice);                
                var medTotal = mainPrescription[i].getElementsByClassName('medTotal')[0].value;
                var lineTotal = Number(mainPrescription[i].getElementsByClassName('lineTotal')[0].innerHTML);
                if (productId){
                    var presMedPrint = xmlReceipt.createElement('span');
                    presMedPrint.setAttribute('align', 'left');
                    presMedPrint.innerHTML = String(medName);
                    receipt.appendChild(presMedPrint);
                    var presLinePrint = xmlReceipt.createElement('line');
                    presLinePrint.innerHTML = '<left>' + String(medTotal) + 'x'+ String(medPrice) + '</left>';
                    presLinePrint.innerHTML += '<right>' + String(lineTotal) + '</right>';
                    receipt.appendChild(presLinePrint);
                }
            };
            var mainServices = document.getElementById('servicesContainer').getElementsByClassName('serviceDetail');
            for (var i=0; i<mainServices.length; i++){
                var xmlServiceName = mainServices[i].getElementsByClassName('serviceName')[0].value;
                var xmlServiceCharge = mainServices[i].getElementsByClassName('serviceCharge')[0].value;
                var xmlService = xmlReceipt.createElement('line');
                xmlServiceName.innerHTML = '<left>'+ String(xmlServiceName) +'</left>' + '<right>' + String(xmlServiceCharge) +'</right>';
                receipt.appendChild(xmlService);
            };
            var xmlConsultationCharge = xmlReceipt.createElement('line');
            xmlConsultationCharge.innerHTML = '<left>Consultation Charge: </left><right>' + String(document.getElementById('consultationCharge').value) + '</right>';
            receipt.appendChild(xmlConsultationCharge);
            var xmlRegistrationCharge = xmlReceipt.createElement('line');
            xmlRegistrationCharge.innerHTML = '<left>Registration Charge: </left><right>' + String(document.getElementById('registrationCharge').value) + '</right>';
            receipt.appendChild(xmlConsultationCharge);
            var xmlRoundOff = xmlReceipt.createElement('line');
            xmlRoundOff.innerHTML = '<left>Round Off: </left><right>' + String(document.getElementById('roundOff').value) + '</right>';
            receipt.appendChild(xmlRoundOff);
            var br = xmlReceipt.createElement('br');
            receipt.appendChild(br);
            var hr = xmlReceipt.createElement('span');
            hr.setAttribute('align', 'center');
            hr.innerHTML = '------------------------------';
            receipt.appendChild(hr);
            var br = xmlReceipt.createElement('br');
            receipt.appendChild(br);
            var xmlTotal = xmlReceipt.createElement('line');
            xmlTotal.setAttribute('size', 'double-height');
            xmlTotal.innerHTML = '<left>Total: </left><right>'+ Number(document.getElementById('amountTotal').innerHTML).toFixed(2) + '</right>';
            receipt.appendChild(xmlTotal);
            var hr = xmlReceipt.createElement('span');
            hr.setAttribute('align', 'center');
            hr.innerHTML = '------------------------------';
            receipt.appendChild(hr);
            var br = xmlReceipt.createElement('br');
            receipt.appendChild(br);
            var xmlPayment = xmlReceipt.createElement('line');
            xmlPayment.innerHTML = '<left>Payment: </left><right>' + Number(document.getElementById('paymentTotal').value).toFixed(2) + '</right>'
            receipt.appendChild(xmlPayment);
            var xmlBalance = xmlReceipt.createElement('line');
            var balanceCalculate = Number(document.getElementById('amountTotal').innerHTML) - Number(document.getElementById('paymentTotal').value)
            xmlBalance.innerHTML = '<left>Balance: </left><right>'+ balanceCalculate.toFixed(2) +'</right>';
            receipt.appendChild(xmlBalance);
            var br = xmlReceipt.createElement('br');
            receipt.appendChild(br);
            console.log(xmlReceipt);
            $.ajax({
                type: "POST",
                processData: false,
                datatype: "json",
                contentType: 'application/json',
                url: "http://127.0.0.1:5000/",
                data: xmlReceipt,
            });
        });
        });
    
});