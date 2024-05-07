import requests

# https://how2electronics.com/send-sensor-data-to-thingspeak-with-raspberry-pi-pico-w/

HTTP_HEADERS = {'Content-Type': 'application/json'}


THINGSPEAK_WRITE_API_KEY = 'T7MQ1G819ZBLSJ12' # BRUKER MIN EGEN!!!
THINGSPEAK_WRITE_URL = f'http://api.thingspeak.com/update?api_key={THINGSPEAK_WRITE_API_KEY}'

def thingspeak_publish_data(data): # Definerer en funskjon som vil eksportere sensordata til Thingspeak i sin egne separate felt
    """
    data = dict(
        bme = dict(temperature=0, humidity=0, pressure=0),
        ens = dict(tvoc=0, eco2=0, rating=''),
        aht = dict(temperature=0, humidity=0),
        )
    """
    payload = {
        'field1' : data["bme"]["temperature"],
        'field2' : data["bme"]["humidity"],
        'field3' : data["bme"]["pressure"],
        'field4' : data["ens"]["tvoc"],
        'field5' : data["ens"]["eco2"],
        'field6' : data["aht"]["temperature"],
        'field7' : data["aht"]["humidity"],
        }
    print(payload)
    r = requests.post(THINGSPEAK_WRITE_URL, json = payload, headers = HTTP_HEADERS) # Funskjon som later som den er en nettleserside
    return r
    
   
    

if __name__ == '__main__': # Testfunksjon som lar oss teste modulen direkte
    from wlan import connect
    sta_if = connect()
    data = dict(
        bme = dict(temperature=0, humidity=0, pressure=0),
        ens = dict(tvoc=0, eco2=0, rating=''),
        aht = dict(temperature=0, humidity=0),
        )
    r = thingspeak_publish_data(data)
    print(r.status_code)
    print(r.text)
    
