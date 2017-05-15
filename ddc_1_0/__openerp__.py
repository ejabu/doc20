{
    "name": "DDC 1.0",
    "version": "0.3.0",
    "depends": ["web_export_view"],
    'author': 'VISI',
    "category":"Document Management",
    "description" : """Simple Document Management""",
    'data': [
        'static_lib.xml',
        #Reports
            #Current Status
                'dash/dash_discipline.xml',
                'dash/dash_exstat.xml',
                'dash/dash_monthly.xml',
                'dash/dash_monthly_conf.xml',
            #Performance
                'dash/dash_delay_approve.xml',
                'dash/dash_delay_approve_conf.xml',
                'dash/dash_pivot_monthly.xml',
            #MDR Overview
                'views/master_deliver_report.xml',
        #Master Document
            #MDR
                'views/master_deliver.xml',
            #Update
                'views/doc_rev_update.xml',
                'views/doc_status_update.xml',

        #Update
            #IDC
                'views/idc_in.xml',
                'views/idc_out.xml',
            #Transmittal
                'views/doc_send.xml',
                'views/doc_send_client.xml',
                'views/doc_rece.xml',

        #Configuration
            'views/conf_master_data.xml',
            'views/conf_rec_comment.xml',

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
