import asyncio
import websockets
from patch import Patch

target = "ws://localhost:8082"
dummy = False

patch = Patch()

async def proxy(ws, path):
  try:
    if 'http' in path:
        target = path.replace('http://', 'ws://').replace('https://', 'wss://')
    async with websockets.connect(target) as ws2:
      while True:
        recver_task = asyncio.ensure_future(ws2.recv())
        sender_task = asyncio.ensure_future(ws.recv())
        done, pending = await asyncio.wait(
          [recver_task, sender_task],
          return_when=asyncio.FIRST_COMPLETED
        )

        if recver_task in done:
          msg = patch.onrecv(ws, recver_task.result())
          print("< {}".format(msg))
          await ws.send(msg)
        else:
          recver_task.cancel()

        if sender_task in done:
          msg = sender_task.result()
          print("> {}".format(msg))
          await ws2.send(patch.onsend(ws, msg))
        else:
          sender_task.cancel()
  except websockets.exceptions.ConnectionClosed:
    pass

async def dummy(ws, path):
  try:
    while True:
      msg = await ws.recv()
      print(">> {}".format(msg))
      await ws.send(msg)
      print("<< {}".format(msg))
  except websockets.exceptions.ConnectionClosed:
    pass

if __name__ == '__main__':
  if dummy:
      target = "ws://localhost:8082"
      dummy_server = websockets.serve(dummy, 'localhost', 8082)
      asyncio.get_event_loop().run_until_complete(dummy_server)
      
  start_server = websockets.serve(proxy, 'localhost', 8081)
  asyncio.get_event_loop().run_until_complete(start_server)
  asyncio.get_event_loop().run_forever()
