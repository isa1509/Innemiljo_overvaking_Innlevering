from time import sleep
import json
from wlan import connect
import uasyncio
from nanoweb import Nanoweb
import urequests

import sensors
from html_functions import naw_write_http_header, render_template
#from leds import blink
import buttons
from thingspeak import thingspeak_publish_data
from machine import WDT

sta_if = connect() # Kobler til trådløst nettverk

naw = Nanoweb() # Lager en instans av Nanoweb

data = dict(
    bme = dict(temperature=0, humidity=0, pressure=0),
    ens = dict(tvoc=0, eco2=0, rating=''),
    aht = dict(temperature=0, humidity=0),
    )

inputs = dict(button_1=False)
    
@naw.route("/") # Lager en nettside
def index(request):
    naw_write_http_header(request)
    html = render_template(
        'index.html',
        temperature_bme=str(data['bme']['temperature']),
        humidity_bme=str(data['bme']['humidity']),
        pressure=str(data['bme']['pressure']),        
        tVOC=str(data['ens']['tvoc']),
        eCO2=str(data['ens']['eco2']),
        temperature_aht=str(data['aht']['temperature']),
        humidity_aht=str(data['aht']['humidity']),
        )
    await request.write(html)


@naw.route("/api/data") # API daten på Pico 'en
def api_data(request):
    naw_write_http_header(request, content_type='application/json')
    await request.write(json.dumps(data))

async def control_loop(): # Sender data til Thingspeak hvert minutt
    while True:
        thingspeak_publish_data(data)
        await uasyncio.sleep_ms(60*1000)

loop = uasyncio.get_event_loop()
loop.create_task(sensors.collect_sensors_data(data, False))
loop.create_task(buttons.wait_for_buttons(inputs))
loop.create_task(naw.run())
loop.create_task(control_loop())

loop.run_forever()
    
