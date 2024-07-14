import openpyxl
from openpyxl import Workbook

workbook = openpyxl.load_workbook('Datenbank.xlsx')
sheet = workbook['HaltestellenSheet']

#wb.save(filename='testExcel.xlsx')




# Correcting the loop to print values from the sheet
for num in range(1, 110):
    cell_a = sheet[f'A{num}'].value
    cell_b = sheet[f'B{num}'].value
    cell_c = sheet[f'C{num}'].value
    cell_d = sheet[f'D{num}'].value
    print(cell_a, cell_b, cell_c, cell_d)

#for num in range(1,10):
#    print(workbook[f'A{num}'].value,workbook[f'B{num}'].value)

#wb.save(filename='testExcel.xlsx')