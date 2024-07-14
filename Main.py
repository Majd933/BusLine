import openpyxl
import openrouteservice as ors
import folium
import pandas as pd
from openpyxl import Workbook


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
    dTestSheet = pd.read_excel(xls, "TestSheet")

#print(dHaltestellenSheet.head(5))
#print(df1["HaltestellenSheet"].at[1,"Haltestellen"])

m = folium.Map(location=(52.1272031, 9.9807198), zoom_start=25, tiles="OpenStreetMap")

## Reading the Value of Cell to get the Cordenation
workbook = openpyxl.load_workbook('Datenbank.xlsx')
sheet = workbook['HaltestellenSheet']

#wb.save(filename='testExcel.xlsx')


# Correcting the loop to print values from the sheet
for num in range(1, 110):
    cell_a = sheet[f'A{num}'].value
    cell_b = sheet[f'B{num}'].value
    cell_c = sheet[f'C{num}'].value
    cell_d = sheet[f'D{num}'].value
    if cell_a == 1:
        folium.Marker(
        location=[cell_c, cell_d],
        tooltip="Click me!",
        popup="Timberline Lodge",
        icon=folium.Icon(color="green"),
    ).add_to(m)
    print(cell_a, cell_b, cell_c, cell_d)

###############################################
## Writing to Excel

## test data:
dHaltestellenSheet = dHaltestellenSheet.head(5)

##with pd.ExcelWriter(excel_file) as writer:
  #dHaltestellenSheet.to_excel(writer, sheet_name="TestSheet")
  ##  df1.to_excel(writer, sheet_name="TestSheet")
dHaltestellenSheet.to_excel('TestResult.xlsx',sheet_name='del',index=False)
##log history

coords = ((9.9807198, 52.1272031), (9.9728696, 52.1340178))

latitude = 52.1272031
longitude = 9.9807198
# key can be omitted for local host
client = ors.Client(key='5b3ce3597851110001cf6248d51314cb052740899c08ab656ca927fe')
routes = client.directions(coords)


#print(df.at[2,'Haltestellen'])
##print(df[['Haltestellen', 'longitude']])

## Universtit :  52.1340178, 9.9728696
## Hansering : 52.1272031,9.9807198


## for loop
"""""
thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print()
"""

##### Folium
#m = folium.Map(location=(52.1272031, 9.9807198), zoom_start=25, tiles="OpenStreetMap")
"""""
folium.Marker(
    location=[52.1272031, 9.9807198],
    tooltip="Click me!",
    popup="Timberline Lodge",
    icon=folium.Icon(color="green"),
).add_to(m)

folium.Marker(
    location=[52.1340178, 9.9728696],
    tooltip="Click me!",
    popup="Timberline Lodge",
    icon=folium.Icon(color="red"),
).add_to(m)
"""""
m.save("D:\Projects\OpenRouteServiceTest\OpenRouteServiceProject\index.html")

m
"""
# Only works if you didn't change the ORS endpoints manually
routes = client.directions(coords)

# If you did change the ORS endpoints for some reason
# you'll have to pass url and required parameters explicitly:
routes = client.request(
  url='/new_url',
  post_json={
      'coordinates': coords,
      'profile': 'driving-car',
      'format': 'geojson'
  })
"""
