from router import Router
import threading

while 1:
  router = Router('127.0.0.1', 4000)

  router.createServer()
  
print('Server shutdown.')
sys.exit()