from router import Router
from profileManager import ProfileManager
from helper import DisplayObjectTable
from routeTable import RoutingTable
from time import sleep

profile = ProfileManager()
profiles = profile.getAllProfiles()
router = Router(profiles['E']['ip'], profiles['E']['port'], 'E')
sleep(5)
router.run()
router.updateRoutingTable()
