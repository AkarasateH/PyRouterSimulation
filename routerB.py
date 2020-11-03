import logging

logging.basicConfig(format='%(asctime)s - Router B:%(message)s', level=logging.INFO)

from router import Router
from profileManager import ProfileManager
from helper import DisplayObjectTable
from routeTable import RoutingTable
from time import sleep

profile = ProfileManager()
profiles = profile.getAllProfiles()
router = Router(profiles['B']['ip'], profiles['B']['port'], 'B')
sleep(5)
router.run()
router.updateRoutingTable()
