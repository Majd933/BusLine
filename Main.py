import openpyxl
import openrouteservice as ors
import folium
import pandas as pd
from openpyxl import Workbook

import ExcelClass as exl


"""""
Zweistufiges Problem:
1.	Strßen:Generierung einer Menge von potentiellen Routen 
2.	Bullinen: Auswahl einer Teilmenge von Routen, die tatsächlich umgesetzt werden sollten (Routenplan)
"""""

#busstation = exl.getBustations()

## reading Xlss data
excel_file = 'Datenbank.xlsx'





##Reading fron Excel
pd.read_excel(excel_file)
# Way 1 (Save the dataframe in variable)
dSheetName = pd.read_excel(excel_file,sheet_name=["HaltestellenSheet"])
##print(dSheetName["HaltestellenSheet"].head(5))
#print(dfile['Haltestellen'].head(5))

dSheetNumber = pd.read_excel(excel_file,sheet_name=[0])
#print(dSheetNumber[0].at[3,"Haltestellen"])
#print(dfile['Haltestellen'].head(5))

dfile = pd.read_excel(excel_file)
#print(dfile.at[3,'Haltestellen'])
#print(dfile.loc[0:5,'Haltestellen'])
#print(dfile['Haltestellen'].head(5))


# Way 2
file = pd.ExcelFile(excel_file)
with pd.ExcelFile(excel_file) as xls:
    dHaltestellenSheet = pd.read_excel(xls, "HaltestellenSheet")
   # dTestSheet = pd.read_excel(xls, "TestSheet")

#print(dHaltestellenSheet.head(5))
#print(df1["HaltestellenSheet"].at[1,"Haltestellen"])

m = folium.Map(location=(52.1272031, 9.9807198), zoom_start=25, tiles="OpenStreetMap")

## Reading the Value of Cell to get the Cordenation
workbook = openpyxl.load_workbook('Datenbank.xlsx')
sheet = workbook['HaltestellenSheet']

#wb.save(filename='testExcel.xlsx')


# Correcting the loop to print values from the sheet
locations = []
for num in range(2, 151):
    cell_a = sheet[f'A{num}'].value
    cell_b = sheet[f'B{num}'].value
    cell_c = sheet[f'C{num}'].value
    cell_d = sheet[f'D{num}'].value

    if isinstance(cell_c, str):
        cell_c = cell_c.replace(',', '.')
    if isinstance(cell_d, str):
        cell_d = cell_d.replace(',', '.')
    location = [float(cell_c), float(cell_d)]
    locations.append(location)

   #### folium.Marker(
     #   location=[float(cell_c), float(cell_d)],
    #    tooltip="Click me!",
    #    popup="Timberline Lodge",
    #    icon=folium.Icon(color="green"),
   ## ).add_to(m)

# Add a line between the nodes
#folium.PolyLine(locations, color="red").add_to(m)
#print(cell_a, cell_b, cell_c, cell_d)

#m.save(r"D:\Projects\OpenRouteServiceTest\OpenRouteServiceProject\index.html")

###############################################
## Writing to Excel

## test data:
dHaltestellenSheet = dHaltestellenSheet.head(5)

##with pd.ExcelWriter(excel_file) as writer:
  #dHaltestellenSheet.to_excel(writer, sheet_name="TestSheet")
  ##  df1.to_excel(writer, sheet_name="TestSheet")
dHaltestellenSheet.to_excel('TestResult.xlsx',sheet_name='del',index=False)
##log history



