import openerp.addons.web.controllers.main as hehe

hehe.Reports.TYPES_MAPPING['xlsx']= 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'



def x_formats(self):
        """ Returns all valid export formats
        :returns: for each export format, a pair of identifier and printable name
        :rtype: [(str, str)]
        """
        return [
            {'tag': 'csv', 'label': 'CSV'},
            {'tag': 'xls', 'label': 'Excel', 'error': None if xlwt else "XLWT required"},
            {'tag': 'xlsx', 'label': 'Excel', 'error': None if xlsxwriter else "XLsxWriter required"},
        ]


hehe.Export.formats = x_formats
