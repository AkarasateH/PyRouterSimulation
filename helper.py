from tabulate import tabulate
import json

def DisplayObjectTable(headers: [str], data: dict, tableName: str = 'Table'):
  primaryKeys = data.keys()
  dataDisplay = []
  
  for key in primaryKeys:
    newArray = [key]
    for val in data[key].values():
      newArray.append(val)
    
    dataDisplay.append(newArray)

  print('\n ----------- {} ----------- '.format(tableName) )
  print(tabulate(dataDisplay, headers=headers, tablefmt='fancy_grid'))

def ConvertJsonToString(data: dict):
  return json.dumps(data)

def ConvertStringToJson(data: str):
  return json.loads(data)
