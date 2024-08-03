import openpyxl
import requests
from openpyxl import Workbook
import openrouteservice as ors
import pandas as pd
from openrouteservice.distance_matrix import distance_matrix
import itertools

#Steps:
# 1. reading the data form the first sheet and save it in dic
# 2. saving this data form dic to the Routes distanze

# 1. reading the data form the first sheet and save it in dic
## reading Xlss data
excel_file = 'Datenbank.xlsx'

workbook = openpyxl.load_workbook('Datenbank.xlsx')

sheetHaltestellen = workbook['HaltestellenSheet']
sheetDistanz = workbook['Distanz']

#workbook = openpyxl.load_workbook('testExcel.xlsx')
#sheetTabelle1 = workbook['Tabelle1']

#wb.save(filename='testExcel.xlsx')

# Dictionary to store coordinates with bus station names
coordinates_dict = {}


## store the first part of coordinates
def storeHaltestellenDictionary ( firstStartStation, firstEndStation, secondStartStation, secondEndStation ):
    for num in range(firstStartStation,firstEndStation):
        cell_a = sheetHaltestellen[f'A{num}'].value
        cell_b = sheetHaltestellen[f'B{num}'].value
        cell_c = sheetHaltestellen[f'C{num}'].value
        cell_d = sheetHaltestellen[f'D{num}'].value

        if isinstance(cell_c, str):
            cell_c = cell_c.replace(',', '.')
        if isinstance(cell_d, str):
            cell_d = cell_d.replace(',', '.')

        try:
            cell_c = float(cell_c)
            cell_d = float(cell_d)
        except ValueError:
            print(f"Skipping invalid coordinates at row {num}: {cell_c}, {cell_d}")
            continue



        # Add coordinates to the dictionary with bus station name as the key
        coordinates_dict[cell_b] = (cell_d, cell_c)

    for num in range(secondStartStation,secondEndStation):
        cell_a = sheetHaltestellen[f'A{num}'].value
        cell_b = sheetHaltestellen[f'B{num}'].value
        cell_c = sheetHaltestellen[f'C{num}'].value
        cell_d = sheetHaltestellen[f'D{num}'].value

        if isinstance(cell_c, str):
            cell_c = cell_c.replace(',', '.')
        if isinstance(cell_d, str):
            cell_d = cell_d.replace(',', '.')

        try:
            cell_c = float(cell_c)
            cell_d = float(cell_d)
        except ValueError:
            print(f"Skipping invalid coordinates at row {num}: {cell_c}, {cell_d}")
            continue



        # Add coordinates to the dictionary with bus station name as the key
        coordinates_dict[cell_b] = (cell_d, cell_c)

#print(coordinates_dict)

#############################################################################################
# 2. saving this data form dic to the Routes distance
# Function to create a distance matrix using OpenRouteService

# Initialize the client
api_key = '5b3ce3597851110001cf6248d51314cb052740899c08ab656ca927fe'
api_key_2 = '5b3ce3597851110001cf624800e182c49d9f477e8ba87982a0acd05b'
client = ors.Client(key=api_key)



## the limit of distance Matrix from the Api is 50-50 Emelent
## Solution: It will divad the complate matrix(150) to sub matrix (25)
## 2. create al posible matrix form the sub matrix = 5 + 4 + 3 + 2 + 1 = 15 Sub matrix
## 1 = 1-50
#   11 = 1-25
#   12 = 26-50

## 2 = 51-100
#   21 = 51-75
#   22 = 76-100

## 3 = 101-150
#   31 = 101-125
#   32 = 126-150

##Steps :
# 11-12 / 11-21 / 11-22 / 11-31 / 11-32
# 12-21 / 12-22 / 12-31 / 12-32
# 21-22 / 21-31 / 21-32
# 22-31 / 22-32
# 31-32

## Note in the list the first line is the Head ( Haltstellename , ...)
## 1-25 / 25-51 / 52-77 / 77-102 / 102-127 / 127-152
# 11-12  : 2-26 + 26-52
# 11-21  : 2-26 + 52-77
# 11-22  : 2-26 + 77-102
# 11-31  : 2-26 + 102-127
# 11-32  : 2-26 + 127-152

# 12-21  : 26-52  + 52-77
# 12-22  : 26-52  + 77-102
# 12-31  : 26-52  + 102-127
# 12-32  : 26-52  + 127-152

# 21-22  : 52-77  + 77-102
# 21-31  : 52-77  + 102-127
# 21-32  : 52-77  + 127-152

# 22-31  : 77-102  + 102-127
# 22-32  : 77-102  + 127-152

# 31-32  : 102-127  + 127-152

# for loop :  26-51:
# list : 26 - 50 = 25 Items
# Excel: Cell 26-50 = 25 Items
## At the beginig take the same  26 -> start with 26 Cell ...
## At the end it will stop 1 cell befor -> if the input 51 -> it will stop at 50
## store the bustation name in list :
subMatrixList = [
             ((1,26), (26,51)),
             ((1,26), (51,76)),
             ((1,26),  (76,101)),
             ((1,26),  (101,126)),
             ((1,26),  (126,150)),
             ((26,51), (51,76)),
             ((26,51), (76,101)),
             ((26,51), (101,126)),
             ((26,51), (126,150)),
             ((51,76), (76,101)),
             ((51,76), (101,126)),
             ((51,76), (126,150)),
             ((76,101), (101,126)),
             ((76,101), (126,150)),
             ((101,126), (126,150)),
        ]

fileNameList = [ "Sub_matrix/Sub_matrix_11-12.xlsx","Sub_matrix/Sub_matrix_11-21.xlsx", "Sub_matrix/Sub_matrix_11-22.xlsx","Sub_matrix/Sub_matrix_11-31.xlsx", "Sub_matrix/Sub_matrix_11-32.xlsx" ,"Sub_matrix/Sub_matrix_12-21.xlsx",
                 "Sub_matrix/Sub_matrix_12-22.xlsx", "Sub_matrix/Sub_matrix_12-31.xlsx", "Sub_matrix/Sub_matrix_12-32.xlsx", "Sub_matrix/Sub_matrix_21-22.xlsx", "Sub_matrix/Sub_matrix_21-31.xlsx", "Sub_matrix/Sub_matrix_21-32.xlsx",
                 "Sub_matrix/Sub_matrix_22-31.xlsx", "Sub_matrix/Sub_matrix_22-32.xlsx", "Sub_matrix/Sub_matrix_31-32.xlsx" ]

def getsubMatrix():
    numOfList=0
    for group in subMatrixList:
        storeHaltestellenDictionary(group[0][0],group[0][1],group[1][0],group[1][1])

        # Prepare the list of coordinates for the API
        coordinates = list(coordinates_dict.values())
        bus_stations = list(coordinates_dict.keys())
        # Make the API call
        matrix = client.distance_matrix(
            locations=coordinates,
            profile='driving-car',
            metrics=['distance'],
            units='m'
        )

        # Check if the response contains the distances key
        if 'distances' in matrix:
            distances = matrix['distances']
        else:
            raise ValueError("No distances found in the response")

        # Create a DataFrame from the distances
        df = pd.DataFrame(distances, index=bus_stations, columns=bus_stations)

        # Save the DataFrame to an Excel file with the sheet name "Table1"
        output_file = fileNameList[numOfList]

        sheetName = str(group)
        df.to_excel(output_file, engine='openpyxl', sheet_name=sheetName)
        #   with pd.ExcelWriter(output_file,mode='a', engine='openpyxl') as writer:
        #    df.to_excel(writer, sheet_name=sheetName)
        print(f"Distance matrix saved to {output_file} in the sheet named {group}")
        numOfList = numOfList+1
        print(group[0][0],group[0][1],group[1][0],group[1][1])
        coordinates_dict.clear()
#print(coordinates_dict)


#getsubMatrix()

#########################################################
# Function to get the Distance Matrix and store it in DateFrame
def getDistanceMatrix():
    df = pd.read_excel('Distance_matrix.xlsx', sheet_name='Distanz')
    df1 = df.set_index("Haltestellen")
    labels = df1.index.tolist()
    #df1 = filterDistanceMatrix(df1)
    #df1 =process_data_frame(df1)
    #df1.to_excel('filteredDistanceMatrix.xlsx', engine='openpyxl')
    print('done')
    return df1.values, labels




# filter to change the distance to 0 if it greater than 1000 -> that mean, there no direct road
def filterDistanceMatrix(df):
    # Nested loop to read the DataFrame
    for index, row in df.iterrows():
        #print(f"Row {index}:")
        for column in df.columns:
            if(df.loc[index,column] > 1000):
                df.loc[index,column] = 0
           # print(f"  {column}: {row[column]}")
        #print(f"\n ***********************************************************")
    # Example usage with your DataFrame
    isolated_nodes, connections = check_connections(df)
    print("Isolated nodes:", isolated_nodes)
    print("Connections per node:", connections)
    # Step 2: Remove the header and the first column to get only the distance matrix
    # df = df.iloc[:, 1:].values  # Skip the first column if it contains row labels
    return df





##Mendelssohnstraße
#Function to check if al node have connection to the Network and there are no isolated_nodes
def check_connections(df):
    nodes = df.index.tolist()
    connections = {node: 0 for node in nodes}

    # Iterate over each node and its distances
    for node in nodes:
        for other_node in nodes:
            if df.loc[node, other_node] > 0:  # Only consider positive distances
                connections[node] += 1
                connections[other_node] += 1

    # Check for nodes with no connections
    isolated_nodes = [node for node, count in connections.items() if count == 0]

    return isolated_nodes, connections


def process_data_frame(df, min_values=4):
    """
    Processes the given DataFrame by applying a filter and extracting the minimum values.

    Parameters:
    df (pd.DataFrame): The input data frame.
    min_values (int): The number of minimum values to extract from each row.

    Returns:
    pd.DataFrame: The new DataFrame with the processed data.
    """

    # Filter function to drop NaN values
    def filter_function(row):
        return row.dropna()

    # Apply the filter function to the DataFrame
    filtered_df = df.apply(filter_function, axis=1)

    # Initialize a list to store the new rows
    new_rows = []

    # Iterate over each row in the filtered DataFrame
    for index, row in filtered_df.iterrows():
        # Get the minimum values from the row
        min_vals = row.nsmallest(min_values)
        # Convert the series to a DataFrame and add it to the list
        min_vals_df = min_vals.to_frame().T
        min_vals_df.index = [index]  # Retain the original index
        new_rows.append(min_vals_df)

    # Concatenate all the rows to form the new DataFrame
    new_df = pd.concat(new_rows, ignore_index=False)

    # Ensure the new DataFrame retains the same columns as the original DataFrame
    new_df = new_df.reindex(columns=df.columns, fill_value=None)

    return new_df


#getDistanceMatrix()