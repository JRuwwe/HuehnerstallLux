# Erstellen Sie ein I2C-Bus-Objekt.
i2c = busio.I2C(board.SCL, board.SDA)

# Erstellen Sie ein TSL2591-Objekt.
sensor = adafruit_tsl2591.TSL2591(i2c)


global OeffnungszeitpktAlt
global SchliessungszeitpktAlt
global klappenzustand
global ZeitTag
global lampenzustand

Oeffnungszeitpkt = None
Schliessungszeitpkt = None
lampeAbendsAnZeit = None
lampenzustand = "undefiniert"
klappenzustand = "undefiniert"

def aendereKlappenzustand():
    global Schliessungszeitpkt
    global Oeffnungszeitpkt
    global klappenzustand

    if sensor.lux < 200 and klappenzustand != "zu":
        time.sleep(10)  # 10sek Warten, wenn dann immernoch Dunkel: Klappe zu!
        if sensor.lux < 200:
            klappenzustand = "zu"
            GPIO.output(S1, 1)
            print("Klappe ist", klappenzustand)
            if Schliessungszeitpkt is None:
                Schliessungszeitpkt = time.time()
                print("Schliessungszeit gesetzt")


    if sensor.lux >= 200 and klappenzustand != "auf":
        time.sleep(10)  # 15min Warten, wenn dann immernoch hell: Klappe auf!
        if sensor.lux >= 200:
            klappenzustand = "auf"
            GPIO.output(S1, 0)
            print("Klappe ist", klappenzustand)
            if Oeffnungszeitpkt is None:
                Oeffnungszeitpkt = time.time()
                print("Oeffnungszeit gesetzt")


def aendereLampenzustand():
    global lampenzustand
    global ZeitTag
    ZeitTag = SchliessungszeitpktAlt - OeffnungszeitpktAlt
    lampeMorgensAnZeitpkt = time.time()

    if ZeitTag < 2100 and sensor.lux < 400:  # Tageslicht weniger als 35min und Deammerung !!400 ist recht hell
        LampeAbendsAnZeitpkt = time.time()
        if LampeAbendsAnZeitpkt < OeffnungszeitpktAlt + ZeitTag+(2100 - ZeitTag)/2:
            GPIO.output(S2, 0)  # Lampe an
            if lampenzustand != "an":
                lampenzustand = "an"
                print("Lampe ist abends angegangen)")
    else:
        GPIO.output(S2, 1)  # Lampe aus
        if lampenzustand != "aus":
            lampenzustand = "aus"
            print("Lampe ist abends ausgegangen")

    if ZeitTag < 2100 and OeffnungszeitpktAlt + ZeitTag+(2100 - ZeitTag)/2 < lampeMorgensAnZeitpkt < OeffnungszeitpktAlt + 3600 - (2100-ZeitTag/2) and sensor.lux < 400:  # !!400 zu hell!?
        GPIO.output(S2, 0)  # Lampe an
        if lampenzustand != "an":
            lampenzustand = "an"
            print("Lampe ist morgens angegangen")
    else:
        GPIO.output(S2, 1)  # Lampe aus
        if lampenzustand != "aus":
            lampenzustand = "aus"
            print("Lampe ist morgens ausgegangen")


try:  # Muss abends nach Sonnenuntergang gestartet werden!

    OeffnungszeitpktAlt = None
    SchliessungszeitpktAlt = None
    while (OeffnungszeitpktAlt is None):
        if (sensor.lux >= 200):  # ist zu Hell!?
            time.sleep(10)
            if (sensor.lux >= 200):
                OeffnungszeitpktAlt = time.time()
                print("Oeffnungszeit Alt gesetzt")
    while (SchliessungszeitpktAlt is None):
        if (sensor.lux < 100): # Ist zu Hell!
            time.sleep(10)
            if(sensor.lux < 100):
                SchliessungszeitpktAlt = time.time()
                print("Schliessungszeit Alt gesetzt")

    while True:
        global zeitdifferenz
        aendereKlappenzustand()
        aendereLampenzustand()

        if Schliessungszeitpkt is not None and Oeffnungszeitpkt is not None:
            zeitdifferenz = Schliessungszeitpkt - Oeffnungszeitpkt
            SchliessungszeitpktAlt = Schliessungszeitpkt
            OeffnungszeitpktAlt = Oeffnungszeitpkt
            # Zeitstempel zuruecksetzen
            Oeffnungszeitpkt = None
            Schliessungszeitpkt = None

        time.sleep(10)

except KeyboardInterrupt:
    print("Das Skript wurde abgebrochen.")
