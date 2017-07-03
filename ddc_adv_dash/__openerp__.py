{
    "name": "DDC Advance Dashboard",
    "version": "0.1",
    'depends': [
        'base',
        'ddc_1_0'
    ],
    'author': 'VISI',
    "category":"Document Dashoard",
    "description" : """Versi 0.1 - Advance Document Management Dashboard""",
    'data': [
        #Security must be Placed on Top
        'static_lib.xml',
        'statReal/view.xml',
        #
    ],
    'demo':[
            #files containing demo data
    ],
    'qweb': [
        'static/src/xml/statReal.xml'
    ],
    'test':[
            #files containing tests
    ],
    'installable' : True,
    'application' : True,
    'auto_install' : False,

}
