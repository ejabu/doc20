def run(wb, ws):
    cell_format = wb.add_format(
                    {'bold': True,
                     'italic': True,
                     'border': 1,
                     'color': '#D7E4BC',
                     })
    c_col = 0
    c_row = 6

    merge_format = wb.add_format({
        'border':   1,
        'align':    'center',
        'valign':   'vcenter',
    })

    ws.merge_range('A7:A8', 'NO', merge_format)
    ws.merge_range('B7:B8', 'NAMA PROJYEK', merge_format)
    ws.merge_range('A9:A11', '1', merge_format)
    ws.merge_range('B9:B11', '-', merge_format)

    ws.merge_range('C7:C8', 'JML DOK', merge_format)

    cell_format = wb.add_format({
                        'align':  'center',
                        'border': 1,
                    })
    ws.write('C9' ,'', cell_format)
    ws.write('C10' ,'A', cell_format)
    ws.write('C11' ,'B', cell_format)

    for col in range(3, 5+1):
        for row in range(6, 10+1):
            ws.write(row, col ,'', cell_format)
