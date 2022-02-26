
import json
import asyncio
import websockets # you gotta 'pip3 install websockets' for this example.

players = {}

# run the socket server
async def update(websocket, path):
    while True:
        message = await websocket.recv()

        if message is None or len(message)<1:
            await websocket.send(json.dumps(players, default=vars))

        data = json.loads( message )

        # print(data['username'])

        # TODO - strip the data. add it to players
        # send all player data out
        # var package = {"username":username,"position":position,"rotation":rotation}

        try:
             players[data['username']]['position'] = data['position']
             players[data['username']]['rotation'] = data['rotation']
        except Exception as e:
             print('player not in list so adding')
             players[data['username']] = {} # 'position': data['position'], 'rotation': data['rotation'] }

        await websocket.send(json.dumps(players, default=vars))

server = websockets.serve(update, '0.0.0.0', 8008)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
