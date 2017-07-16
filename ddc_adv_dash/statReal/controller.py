from openerp import http
import json
from openerp.tools import ustr
from openerp.http import request, serialize_exception as _serialize_exception
from openerp.tools.misc import xlwt
from cStringIO import StringIO
from collections import deque

from datetime import datetime


try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None

class TableExporter(http.Controller):

    @http.route('/web/pivot/check_xlwt', type='json', auth='none')
    def check_xlwt(self):
        return xlwt is not None


    @http.route('/web/adv/stat_real', type='http', auth="user")
    def export_xls(self, data, token):


        style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
            num_format_str='#,##0.00')
        style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

        wb = xlwt.Workbook()
        ws = wb.add_sheet('A Test Sheet')

        ws.write(0, 0, 1234.56, style0)
        ws.write(1, 0, datetime.now(), style1)
        ws.write(2, 0, 1)
        ws.write(2, 1, 1)
        ws.write(2, 2, xlwt.Formula("A3+B3"))

        wb.save('example.xls')

        response = request.make_response(None,
            headers=[('Content-Type', 'application/vnd.ms-excel'),
                    ('Content-Disposition', 'attachment; filename=table.xls;')],
            cookies={'fileToken': token})
        wb.save(response.stream)

        return response
