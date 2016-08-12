from wsmitmproxy import patch, proxy
import asyncio
import websockets
import getopt
import sys

def shell():
  bind_address = None
  port = 8081

  opts,args = getopt.getopt(sys.argv[1:], 'b:s:p:', ['--bind-address', '--script', '--port'])
  for o,a in opts:
    if o in ('-b', '--bind-address'): proxy.patches.append(patch.Patch(a))
    if o in ('-s', '--script'): proxy.patches.append(patch.Patch(a))
    if o in ('-p', '--port'):   port = int(a)

  start_server = websockets.serve(proxy.proxy, bind_address, port)
  asyncio.get_event_loop().run_until_complete(start_server)
  asyncio.get_event_loop().run_forever()
