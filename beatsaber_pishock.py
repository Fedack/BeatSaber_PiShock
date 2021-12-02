import asyncio
import websockets
import json
import aiohttp
import aiohttp_requests
import datetime
import random
import traceback

configs = None
lastused = datetime.datetime.now()
lastused = float(datetime.datetime.timestamp(lastused))
lastused = datetime.datetime.fromtimestamp(lastused)
nextmiss = lastused + datetime.timedelta(seconds=1)
lastused_bomb = datetime.datetime.now()
lastused_bomb = float(datetime.datetime.timestamp(lastused_bomb))
lastused_bomb = datetime.datetime.fromtimestamp(lastused_bomb)
nextmiss_bomb = lastused + datetime.timedelta(seconds=1)
combo = 0
last_intensity = 0


def load_configs(path):
    global configs
    json_file = open(path, 'r')
    configs = json.load(json_file)
    json_file.close()


async def sendCommand(target: str, payload):
    response = await aiohttp_requests.requests.post(target, json=payload)
    text = await response.text()
    print(text)


async def hit(perf, fail):
    global last_intensity
    target = configs['Target'] + configs['Hit']['Path']
    intensity = combo * configs['Hit']['Mult']
    if(intensity > 100):
        intensity = 100
    if(fail):
        intensity = 0
    hitPayload = configs['Hit']['Params']
    payload = {**configs['Params'], **
               hitPayload, "Intensity": intensity, "Op": 0}
    print(f'Setting vibration to for buttplug to {intensity}')
    await sendCommand(target, payload)


async def miss(perf, eventType):
    global combo
    target = configs['Target'] + configs[eventType]['Path']
    mode = configs[eventType]['Mode']
    intensity = 100
    if(mode == 0):
        intensity = configs[eventType]['0Static']
    elif(mode == 1):
        min = configs[eventType]['1Random']['Min']
        max = configs[eventType]['1Random']['Max']
        intensity = random.randint(min, max)
    elif(mode == 2):
        comboCurrent = combo * configs[eventType]['2Combo']['Mult']
        max = configs[eventType]['2Combo']['Max']
        if(comboCurrent < max):
            intensity = comboCurrent
        else:
            intensity = max
    elif(mode == 3):
        comboCurrent = combo * configs[eventType]['3InvCombo']['Mult']
        max = configs[eventType]['3InvCombo']['Max']
        min = configs[eventType]['3InvCombo']['Min']
        currentInt = max - comboCurrent
        if (currentInt > min):
            intensity = currentInt
        else:
            intensity = min
    missPayload = configs[eventType]['Params']
    if(configs['UsePiShock']):
        code = configs[eventType]['Params']['Code']
        if isinstance(code, str):
            missPayload = configs[eventType]['Params']
        elif isinstance(code, list):
            op = configs[eventType]['Params']['Op']
            duration = configs[eventType]['Params']['Duration']
            missPayload = {"Op": op,
                           "Duration": duration, "Code": random.choice(code)}
    payload = {**configs['Params'], **
               missPayload, "Intensity": intensity}
    combo = 0
    print(f"Sending {intensity} using mode {mode}")
    await sendCommand(target, payload)


async def consumer_handler(websocket: websockets.WebSocketClientProtocol) -> None:
    async for message in websocket:
        global combo
        #json_mylist = json.dumps(message)
        json_obj = json.loads(message)
        #print(f"< {json_mylist}")
        if(json_obj['event'] == 'noteMissed'):
            note_missed = json_obj['status']['performance']['missedNotes']
            print(f'Whoops! Note Missed! Total Missed {note_missed}')
            global nextmiss
            if(datetime.datetime.now() > nextmiss):
                print('Not On Cooldown')
                await miss(json_obj['status']['performance'], 'Miss')
                cooldown = configs['Miss']['Cooldown']
                lastused = datetime.datetime.now()
                lastused = float(datetime.datetime.timestamp(lastused))
                lastused = datetime.datetime.fromtimestamp(lastused)
                nextmiss = lastused + datetime.timedelta(seconds=cooldown)
            else:
                print('On Cooldown, Lucky you.')
            if(configs['Hit']['Active']):
                await hit(json_obj['status']['performance'], True)
        elif((json_obj['event'] == 'bombCut') or (json_obj['event'] == 'obstacleEnter')):
            bomb_cut = json_obj['status']['performance']['missedNotes']
            print(f'Whoops! Note Missed! Total Missed {bomb_cut}')
            global nextmiss_bomb
            if(datetime.datetime.now() > nextmiss_bomb):
                print('Not On Cooldown')
                await miss(json_obj['status']['performance'], 'Miss')
                cooldown = configs['Bomb']['Cooldown']
                lastused_bomb = datetime.datetime.now()
                lastused_bomb = float(
                    datetime.datetime.timestamp(lastused_bomb))
                lastused_bomb = datetime.datetime.fromtimestamp(lastused_bomb)
                nextmiss_bomb = lastused_bomb + \
                    datetime.timedelta(seconds=cooldown)
            else:
                print('On Cooldown, Lucky you.')
            if(configs['Hit']['Active']):
                await hit(json_obj['status']['performance'], True)
        elif(json_obj['event'] == 'scoreChanged'):
            combo = json_obj['status']['performance']['combo']
        if(json_obj['event'] == 'noteFullyCut'):
            combo = json_obj['status']['performance']['combo']
            if(configs['Hit']['Active']):
                await hit(json_obj['status']['performance'], False)


async def consume(hostname: str, port: int, extension: str) -> None:
    try:
        websocket_resource_url = f"ws://{hostname}:{port}/{extension}"
        async with websockets.connect(websocket_resource_url) as websocket:
            print('Connection Established!')
            await consumer_handler(websocket)
    except Exception as e:
        traceback.print_exc()
        await asyncio.sleep(5)
        await consume(hostname, port, extension)


if __name__ == '__main__':
    print('starting')
    load_configs('config.json')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume("localhost", 6557, "socket"))
    loop.run_forever()
