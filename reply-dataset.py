import asyncio
import nest_asyncio
nest_asyncio.apply()
import websockets
import json
from threading import Timer
import requests
import re
# Discord Botis Tokeni
token = ""

# Serverebi Sadac Movakhdent Replys Monitorings
monitored_servers = ["1111111111111111","22222222222222"] 

# Informacia Rac Unda Gavugzvnot Discords Rom Shevidet Botis Akauntze
payload = '{"op":2,"d":{"token":"'+token+'","intents":3276799,"properties":{"os":"linux","browser":"my_library","device":"my_library"},"presence":{"activities":[{"name":"gitvaltvaleb","type":0}],"status":"","since":91879201,"afk":false}}}'

async def connect_to_gateway():
    uri = "wss://gateway.discord.gg/?v=10&encoding=json"
    async with websockets.connect(uri, max_size=None) as websocket:
        await websocket.send(payload)
        while True:
            
            message = await websocket.recv()    # Amit Vigebt Ras Gvibrunebs Discordis WebSocketi
            load = json.loads(message)          # Vakcevt Mesijs Rogorc Json Rom Davparsot
            t = load["t"]                       # Amit Vigebt Romel Gateway Events Abrunebs Mesijad Anu Ra Ikneba d Shi Gamosaxuli
            match load["op"]:
                case 10:
                    __heartbeat = load["d"]["heartbeat_interval"]/1000 # d Sheicavs Im Informacias Rasac Discordis Websocketi Abrunebs
                    async def func_wrapper():
                        while True:
                            await asyncio.sleep(__heartbeat)
                            await websocket.send('{"op": 1, "d": null}') # Vugzavnit Discords Rom Sheinarchunos Chventan Kavshiri Da Rom Isev Cocxalni Vart
                            print("shoki chavartkit shoki (defibrillator) (defibliracia) XDDDD gulis cema gaugrdzelda")
                    print(load["d"]["heartbeat_interval"]) #debug
                    asyncio.create_task(func_wrapper())
                    #t = Timer(load["d"]["heartbeat_interval"]/1000, func_wrapper)
                    #t.start()
            match t:
                case "READY":
                    print("Boti Chartulia")
                case "MESSAGE_CREATE":
                    message = load["d"]["content"]          # Mesijis Shemcveloba

                    if 'referenced_message' in load["d"] and not 'bot' in load["d"]["author"] and 'guild_id' in load["d"]: # Sanity Checks, reply check, bot check, DM check
                        for monitored_server_id in monitored_servers: # Vighebt Im Serverebs Sadac Unda Movaxdinont Monitireba
                            if load["d"]["guild_id"] == monitored_server_id and not re.match("<@!*&*[0-9]+>",message): # Vamowmebt Mesijis Serveri Ari Tu Ara Listshi, Vamowmebt Aris Mesijshi Mention Tu Ara
                                with open("data.json", 'r',encoding="utf8") as file: # Ak Vaseivebt Ukve
                                    data = json.load(file)
                                data.append({"resp":load["d"]["content"], "msg":load["d"]["referenced_message"]["content"]})
                                print({"resp":load["d"]["content"], "msg":load["d"]["referenced_message"]["content"]}) # DEBUG
                                with open("data.json", 'w',encoding="utf8") as file:
                                    json.dump(data, file, indent=4)



print(__name__)
asyncio.get_event_loop().run_until_complete(connect_to_gateway())
