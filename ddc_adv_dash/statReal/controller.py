from openerp import http
import json
from openerp.tools import ustr
from openerp.http import request, serialize_exception as _serialize_exception
from openerp.tools.misc import xlwt
from cStringIO import StringIO
from collections import deque

import json
from datetime import datetime


try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None

import openerp.addons.web.controllers.main as hehe


class TableExporter(http.Controller):

    @http.route('/web/pivot/check_xlwt', type='json', auth='none')
    def check_xlwt(self):
        return xlwt is not None

    @http.route('/web/adv/stat_real', type='http', auth="user")
    def export_xlsx(self, data, token):
        fp = StringIO()
        import ipdb; ipdb.set_trace()
        data = json.loads(data)

        workbook = xlsxwriter.Workbook(fp)
        worksheet = workbook.add_worksheet("Status Realisasi")

        format = workbook.add_format()

        format.set_font_color('red')

        worksheet.write(10, 10, 'wheelbarrow', format)

        worksheet.set_column('C:W', 4.9)

        worksheet.write('A1', 123)

        merge_format = workbook.add_format({
            'font_size': 24,
            'align':    'center',
            'valign':   'vcenter',
            # 'bold':     True,
            # 'border':   6,
            # 'fg_color': '#D7E4BC',
        })

        worksheet.merge_range('C2:S4', 'STATUS REALISASI DOKUMEN ENGINEERING', merge_format)
        workbook.close()
        fp.seek(0)
        data = fp.read()

        response = request.make_response(data,
            headers=[('Content-Type', 'application/vnd.ms-excel'),
                    ('Content-Disposition', 'attachment; filename=Status Realisasi.xlsx;')],
        cookies={'fileToken': token})



        return response
