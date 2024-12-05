import asyncio
import nest_asyncio
nest_asyncio.apply()
import websockets
import json
from threading import Timer
import requests

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Discord Botis Tokeni
token = ""

# Vtvirtavt Models
model = load_model('ams.h5')

# Vtvirtavt Modelis Gamomtvlel Informacias
with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)
with open('label_encoder.pkl', 'rb') as handle:
    label_encoder = pickle.load(handle)
max_len = model.input_shape[1]

# Mtavari Nawili Sadac Xdeba Modelisgan Teqstis Gamogheba
def generate_response(user_input):
    seq = tokenizer.texts_to_sequences([user_input])
    padded_seq = pad_sequences(seq, maxlen=max_len, padding='post')
    predictions = model.predict(padded_seq)
    confidence = np.max(predictions)
    response_index = np.argmax(predictions)
    response = label_encoder.inverse_transform([response_index])[0]
    return response, confidence

# Informacia Rac Unda Gavugzvnot Discords Rom Shevidet Botis Akauntze
payload = '{"op":2,"d":{"token":"'+token+'","intents":3276799,"properties":{"os":"linux","browser":"my_library","device":"my_library"},"presence":{"activities":[{"name":"gitvaltvaleb","type":0}],"status":"","since":91879201,"afk":false}}}'

async def connect_to_gateway():
    uri = "wss://gateway.discord.gg/?v=10&encoding=json"
    async with websockets.connect(uri) as websocket:
        await websocket.send(payload)
        while True:
            
            message = await websocket.recv()    # Amit Vigebt Ras Gvibrunebs Discordis WebSocketi
            load = json.loads(message)          # Vakcevt Mesijs Rogorc Json Rom Davparsot
            t = load["t"]                       # Amit Vigebt Romel Gateway Events Abrunebs Mesijad Anu Ra Ikneba d Shi Gamosaxuli
            print(load)
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
                    channel_id = load["d"]["channel_id"]    # Chaneli Saidanac Mesiji Gamoigzavna
                    match message:
                        case "<@1207445278588932127>":      # Chemi Mention Gamosaxuli Rogorc Mesiji
                            print(1)    
                            headers = {
                                "Authorization": f"Bot {token}"
                            }
                            data = {
                              "content": "chem umfros nu awuxeb oe",
                            }
                            #requestis droa
                            requests.post(f"https://discord.com/api/v9/channels/{channel_id}", headers=headers, data=data)
                        case _:
                            if load["d"]["channel_id"] == "1250094075688910859" and load["d"]["author"]["id"] != "1222697100245078117":
                                headers = {
                                    "Authorization": f"Bot {token}"
                                }
                                resp, conf = generate_response(load["d"]["content"])
                                data = {
                                  "content": f"{resp} `{conf * 100:.2f}%`",
                                }
                                
                                requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, data=data)
                            elif not load["d"]["channel_id"] == "1250094075688910859": # Vagrovebt Informacias Shemdgomi Trainingistvis
                                with open("data.json", 'r',encoding="utf8") as file:
                                    data = json.load(file)
                                data.append({"msg":load["d"]["content"]})
    
                                with open("data.json", 'w',encoding="utf8") as file:
                                    json.dump(data, file, indent=4)


print(__name__)
asyncio.get_event_loop().run_until_complete(connect_to_gateway())
