#This file main purpose is for Configuring EXCEL REPORT 
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

        import xlsxwriter
        from lib import title
        from lib import side_column
        from lib import content
        from lib import set_width
        from datetime import datetime

        data = json.loads(data)

        wb = xlsxwriter.Workbook(fp)
        ws = wb.add_worksheet("Status Realisasi")
        now =  datetime.now().strftime("%Y-%m-%d %H-%M-%S")

        filename = 'output/Status Realisasi ' + now + '.xlsx'
        att_string = 'attachment; filename=Status Realisasi ' + now + '.xlsx;'

        title.run(wb, ws)
        side_column.run(wb, ws)
        content.run(wb, ws, data)
        set_width.run(wb, ws)

        wb.close()
        fp.seek(0)
        data = fp.read()

        response = request.make_response(data,
            headers=[('Content-Type', 'application/vnd.ms-excel'),
                    ('Content-Disposition', att_string)],
        cookies={'fileToken': token})



        return response
