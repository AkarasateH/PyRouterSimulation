#!/bin/bash
echo -n "---- Setting Profiles ----"
python3 ~/Learning/S-MCS_Work/ComNetwork/PyRouterSimulation/setting.py

echo -n "---- Running Routers ----"

osascript -e 'tell app "Terminal"
    do script "cd ~/Learning/S-MCS_Work/ComNetwork/PyRouterSimulation/ && python3 routerA.py"
end tell'

osascript -e 'tell app "Terminal"
    do script "cd ~/Learning/S-MCS_Work/ComNetwork/PyRouterSimulation/ && python3 routerB.py"
end tell'

osascript -e 'tell app "Terminal"
    do script "cd ~/Learning/S-MCS_Work/ComNetwork/PyRouterSimulation/ && python3 routerC.py"
end tell'

# osascript -e 'tell app "Terminal"
#     do script "cd ~/Learning/S-MCS_Work/ComNetwork/PyRouterSimulation/ && python3 routerD.py"
# end tell'

# osascript -e 'tell app "Terminal"
#     do script "cd ~/Learning/S-MCS_Work/ComNetwork/PyRouterSimulation/ && python3 routerE.py"
# end tell'

# osascript -e 'tell app "Terminal"
#     do script "cd ~/Learning/S-MCS_Work/ComNetwork/PyRouterSimulation/ && python3 routerF.py"
# end tell'

echo -n "---- All router are running successfully ----"