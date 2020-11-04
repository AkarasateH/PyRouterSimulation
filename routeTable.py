import logging
from helper import DisplayObjectTable 

logging.getLogger('Routing Table:')

class RoutingTable:
  def __displayTable(self):
    DisplayObjectTable(['Dest Subnet', 'Next Hop', 'Cost'], self.table, 'Routing Table ' + self.owner)

  def __init__(self, routerName: str, subnets: [str]):
    logging.info('Created routing table for router {} subnet {}'.format(routerName, subnets))
    self.owner = routerName
    self.table = {}

    for subnet in subnets:
      self.table[subnet] = {
        'nextHop': '-',
        'cost': 1
      }
    self.__displayTable()

  # Remove link in the table by subnet
  def removeLinkBySubnet(self, subnet: str):
    self.table.pop(subnet)

  def subnetIsFound(self, subnet: str):
    return True if subnet in self.table.keys() else False

  def getLinkDetailBySubnet(self, subnet: str):
    return {
      'owner': self.owner,
      'linkDetail': self.table.get(subnet, None)
    }

  def __updateTableBySubnet(self, subnet: str, nextHop: str, cost: int):
    self.table[subnet] = {
      'nextHop': nextHop,
      'cost': cost
    }

    return self.table[subnet]

  # tableData should have this format { subnet, cost, owner }
  def updateTable(self, tableData: {
    'subnet': str,
    'cost': int,
    'owner': str
  }):
    if not tableData['subnet'] in self.table:
      self.__updateTableBySubnet(tableData['subnet'], tableData['owner'], tableData['cost'])
    elif tableData['cost'] < self.table[tableData['subnet']]['cost']:
      self.__updateTableBySubnet(tableData['subnet'], tableData['owner'], tableData['cost'])
    
    self.__displayTable()
