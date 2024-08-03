
#   List  = [] ordered and changeable. Duplicates OK
#   Set   = {} unordered and immutable, but Add/Remove OK. NO duplicates
#   Tuple = () ordered and unchangeable. Duplicates OK. FASTER

##https://www.youtube.com/watch?v=kbyHLU9JqjE&list=PLZPZq0r_RZOOkUQbat8LyQii36cJf2SWT&index=22

#Helpe Mtehod: List / Set / Tuple
##listTest = ["Apple" , "Orange"]
#setTest = {"Apple" , "Orange"}
#tupleTest = ("Apple" , "Orange")

#print(dir(listTest))
##print(help(listTest))




#dictionary =  a collection of {key:value} pairs ordered and changeable. No duplicates
#https://www.youtube.com/watch?v=MZZSMaEAC2g&list=PLZPZq0r_RZOOkUQbat8LyQii36cJf2SWT&index=25

#capitals = {"USA": "Washington D.C.",
#                    "India": "New Delhi",
#                   "China": "Beijing",
#                   "Russia": "Moscow"}

#print(dir(capitals))
#print(help(capitals))

##capitals.update({"Germany": "Berlin"})


# disply the art of list

def add(*nums: int) -> int:
    total = 0
    for num in nums:
        total += num
    return total

print(add(1, 2, 3, 4))  # Output: 10



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
folium.PolyLine(locations, color="red").add_to(m)
print(cell_a, cell_b, cell_c, cell_d)

m.save(r"D:\Projects\OpenRouteServiceTest\OpenRouteServiceProject\index.html")

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


# Example usage
#coordinates_dict = {
#    "Station A": (40.712776, -74.005974),
#    "Station B": (34.052235, -118.243683),
#    "Station C": (51.507351, -0.127758)
#}

# Request distance matrix from OpenRouteService
matrix = client.distance_matrix(
        locations=coordinates,
    ## muss sein : locations=[[9.70093,48.477473],[9.207916,49.153868]]
        profile='driving-car',
        metrics=['distance'],
        units='m'
    )
# Initialize an empty DataFrame for the distance matrix
distance_matrix = pd.DataFrame(index=bus_stations, columns=bus_stations)
#Extract the distance from the response (in meters)
print(distance_matrix)
# return distance_matrix


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


"""
# Function to get the Distance Matrix and store it in DateFrame

def getDistanceMatrix() :
    df = pd.read_excel('Distance_matrix_symmetric.xlsx', sheet_name='Distanz')

   # print(df.values[0][0])
   # print(df.shape)
   # print(df.index)
    df1 = df.set_index("Haltestellen")
    #print(df1.index)
    #print(df1.index)
    #print(df1.columns)
    #print(df1['Halle 39'][1])
    ##to access Row
    #print(df.iloc[1])
    ## to accses columnsPauluskirche
    #pd.set_option('display.max_rows', 150)
    #pd.set_option('display.max_columns', 150)
    #print(df1.loc['Flugplatz','Linnenkamp'])
    #print(df1)

    filterDistanceMatrix(df1)
    return df1.values
"""