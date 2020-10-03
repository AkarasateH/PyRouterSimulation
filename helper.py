from tabulate import tabulate

def DisplayObjectTable(headers: [str], data: dict):
  primaryKeys = data.keys()
  dataDisplay = []
  
  for key in primaryKeys:
    newArray = [key]
    for val in data[key].values():
      newArray.append(val)
    
    dataDisplay.append(newArray)

  print(tabulate(dataDisplay, headers=headers, tablefmt='fancy_grid'))