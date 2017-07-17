def run(wb, ws):
    merge_format = wb.add_format({
        'font_size': 24,
        'align':    'center',
        'valign':   'vcenter',
        # 'bold':     True,
        # 'border':   6,
        # 'fg_color': '#D7E4BC',
    })

    ws.merge_range('C2:S4', 'STATUS REALISASI DOKUMEN ENGINEERING', merge_format)
