{
    "name": "DDC 1.0",
    "version": "0.2.0",
    "depends": ["web_export_view"],
    'author': 'VISI',
    "category":"Document Management",
    "description" : """Simple Document Management""",
    'data': [
        'static_lib.xml',
        'dash/dash_discipline.xml',
        'dash/dash_exstat.xml',
        'dash/dash_delay_approve.xml',
        'dash/dash_delay_approve_conf.xml',
        'dash/dash_monthly.xml',
        'dash/dash_monthly_conf.xml',
        'dash/dash_pivot_monthly.xml',
        'views/master_deliver.xml',
        'views/master_deliver_report.xml',
        'views/conf_rec_comment.xml',
        'views/doc_idc.xml',
        'views/doc_send.xml',
        'views/doc_rece.xml',
        'views/doc_status_update.xml',
        'views/conf_master_data.xml',
        'views/menus.xml',
    ],
    'demo':[
            #files containing demo data
    ],
    'test':[
            #files containing tests
    ],
    'installable' : True,
    'application' : True,
    'auto_install' : False,

}
