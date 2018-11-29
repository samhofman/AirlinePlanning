# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import xlrd as xl

book = xl.open_workbook('Datasheet.xlsx')


def get_cell_range(sheet, start_col, start_row, end_col, end_row):
    return [book.sheet_by_index(sheet-1).row_values(row, start_colx=start_col, end_colx=end_col+1) for row in xrange(start_row, end_row+1)]


airport_data = get_cell_range(2, 2, 6, 26, 9)   # C7 to Z10

demand_pw = get_cell_range(2, 2, 15, 21, 34)    # C16 to V35

demand_pw_hs = get_cell_range(2, 2, 37, 26, 60) # C38 to Z61

demand_ow_ls = get_cell_range(2, 2, 63, 26, 86) # C64 to Z87

competition = get_cell_range(2, 2, 89, 26, 112) # C90 to Z113 









