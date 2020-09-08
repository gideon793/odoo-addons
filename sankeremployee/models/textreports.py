# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
_logger = logging.getLogger(__name__)



class textreport(models.Model):
    _name = 'sankerempoloyee.textreport'
    filetest = fields.Binary('Text File', readonly=True)
    filename = fields.Char('Filename')


    @api.multi
    def textreport(self):
        _logger.info('textreport')
        file = open("newfile.txt", "w")
        file.write("hello world in the new file")
        file.write("and another line")
        file.close()
        filedata = file.read()
        values = {
            'name': "Name of text file.txt",
            'datas_fname': 'print_file_name.txt',
            'res_model': 'ir.ui.view',
            'res_id': False,
            'type': 'binary',
            'public': True,
            'datas': base64.b64encode(filedata),

        }
        attachment_id = self.env['ir.attachment'].sudo().create(values)
        download_url = '/web/content/' + str(attachment_id.id) + '?download=True'
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }


