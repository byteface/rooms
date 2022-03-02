
import json
import asyncio
import websockets  # you gotta 'pip3 install websockets' for this example.
import datetime

players = {}

# run the socket server
async def update(websocket, path):
    while True:
        message = await websocket.recv()

        if message is None or len(message) < 1:
            await websocket.send(json.dumps(players, default=vars))

        data = json.loads(message)

        try:
            # players[data['username']]['name'] = data['name']
            players[data['username']]['position'] = data['position']
            players[data['username']]['rotation'] = data['rotation']
            # add a last_update time to the player
            players[data['username']]['last_update'] = str(datetime.datetime.now())
        except Exception as e:
            print('player not in list so adding')
            players[data['username']] = {}  # 'position': data['position'], 'rotation': data['rotation'] }

        # remove the player from the list we we get a disconnect message
        # try:
        #     if data['disconnect'] == True:
        #         print('removing player')
        #         del players[data['username']]
        # except Exception as e:
        #     pass

        # add a timeout to remove the player from the list
        dead_players = []
        for player in players:
            try:
                last_update = datetime.datetime.strptime(players[player]['last_update'], '%Y-%m-%d %H:%M:%S.%f')
                if datetime.datetime.now() - last_update > datetime.timedelta(seconds=5):
                    print('removing player')
                    # del players[player]
                    dead_players.append(player)
            except KeyError:
                pass
            except Exception as e:
                pass
        for player in dead_players:
            del players[player]

        await websocket.send(json.dumps(players, default=vars))

server = websockets.serve(update, '0.0.0.0', 8008)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
