from xlsxwriter.utility import xl_rowcol_to_cell

def run(wb, ws, data):

    c_col = 6
    c_row = 6

    start_col = 6
    start_row = 6

    index=0
    color=["#BFBFBF", "#92D050", "#BDD7EE", "#FCE4D6", "#FFF2CC"]
    len_color = len(color)

    cell_format = wb.add_format({
                                 'border': 1,
                                'align':   'center',
                             })
    red_format = wb.add_format({
                                 'border': 1,
                                'align':   'center',
                                'bg_color': '#FCE4D6',
                             })
    for rec in data:
        header_format = wb.add_format({
            'align':    'center',
            'valign':   'vcenter',
            'border':   1,
            'fg_color': color[int(index % len_color)],
        })

        ws.merge_range(c_row, c_col, c_row, c_col+3, rec['week_name'], header_format)



        ws.write(c_row+1, c_col ,"IFI", cell_format)
        ws.write(c_row+1, c_col+1 ,"IFR", cell_format)
        ws.write(c_row+1, c_col+2 ,"IFA", cell_format)
        ws.write(c_row+1, c_col+3 ,"AFC", cell_format)

        ws.write(c_row+2, c_col ,rec['ifi'], cell_format)
        ws.write(c_row+2, c_col+1 ,rec['ifr'], cell_format)
        ws.write(c_row+2, c_col+2 ,rec['ifa'], cell_format)
        ws.write(c_row+2, c_col+3 ,rec['afc'], cell_format)

        ws.write(c_row+3, c_col ,"", cell_format)
        ws.write(c_row+3, c_col+1 ,rec['def_ifr'], cell_format)
        ws.write(c_row+3, c_col+2 ,rec['def_ifa'], cell_format)
        ws.write(c_row+3, c_col+3 ,rec['def_afc'], cell_format)

        ws.write(c_row+4, c_col ,rec['diff_ifi'], cell_format)
        ws.write(c_row+4, c_col+1 ,rec['diff_ifr'], cell_format)
        ws.write(c_row+4, c_col+2 ,rec['diff_ifa'], cell_format)
        ws.write(c_row+4, c_col+3 ,rec['diff_afc'], cell_format)



        c_col+=4
        index+=1



    end_col = c_col
    end_row = c_row + 4

    #Edit Column Width
    ws.set_column(6, end_col-1, 4.91)
    ws.set_column(end_col, end_col, 6.71)

    #Make Conditional Formatting
    conditional_format = {
                            'type' : 'cell',
                            'criteria': 'less than',
                            'value':    0,
                            'format':   red_format
                            }
    ws.conditional_format(start_row+2, start_col, end_row, end_col, conditional_format)


    #FIX
    cell_format = wb.add_format({
                        'align':  'center',
                        'border': 1,
                    })
    ws.write('C9' ,'20', cell_format)

    #Make Row
    perc_format = wb.add_format({
        'border':   1,
        'align':    'center',
        'valign':   'vcenter',
    })

    ws.merge_range(start_row,end_col, start_row+1, end_col, "%", perc_format)

    perc_cell = xl_rowcol_to_cell(start_row+2, end_col-1)
    perc_formula="=" + perc_cell + "/C9"


    perc_format = wb.add_format({
                                    'align':    'center',
                                    'border':   1,
                                    'num_format': '0.0%'
                                    })
    ws.write_formula(start_row+2, end_col, perc_formula, perc_format)
    ws.write_formula(start_row+3, end_col, "", cell_format)
    ws.write_formula(start_row+4, end_col, "", cell_format)
