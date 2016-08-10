from wsproxy import proxy
import asyncio
import websockets

def shell():
  start_server = websockets.serve(proxy.proxy, 'localhost', 8081)
  asyncio.get_event_loop().run_until_complete(start_server)
  asyncio.get_event_loop().run_forever()
