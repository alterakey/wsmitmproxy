import asyncio
import websockets
from wsmitmproxy.patch import Patch

target = "ws://localhost:8082"

patches = []

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
          msg = recver_task.result()
          for patch in patches:
            msg = patch.call('onrecv', ws, msg)
          print("< {}".format(msg))
          await ws.send(msg)
        else:
          recver_task.cancel()

        if sender_task in done:
          msg = sender_task.result()
          print("> {}".format(msg))
          for patch in patches:
            msg = patch.call('onsend', ws, msg)
          await ws2.send(msg)
        else:
          sender_task.cancel()
  except websockets.exceptions.ConnectionClosed:
    pass
