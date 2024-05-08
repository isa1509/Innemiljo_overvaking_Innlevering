import network 
import time

SSID = 'DATO IOT' # Navn på nettverk som skal brukes 
PASSWORD = 'Admin:123' # Passord på nettverk som skal brukes

def connect(): # Funskjon som gir ifra en melding eller "feilmelding" avhengig av om enheten kobler seg til nettverket innafor tidsrammen
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        c = 0
        while sta_if.isconnected() == False:
            c += 1
            time.sleep(0.2)
            if c > 50:
                print('Connection failed')
                break
        if c <= 50:
            print('Connection successful')
    else:
        print('Already connected!') # Gir forskellig melding hvis man allerede er tilkoblet 
    print(sta_if.ifconfig())
    return sta_if

if __name__ == '__main__': # Testfunskjon som lar deg teste modulen direkte
    sta_if = connect()
    nets = sta_if.scan()
    for n in nets:
        print(n)