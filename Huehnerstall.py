# Imports können nur am Raspberry funktionieren, Fehlermeldungen am PC normal
import datetime

import RPi.GPIO as GPIO
import board
import adafruit_tsl2591
import busio
import time


# S1 ist die Steckdose am naechsten zu den Verteilerdosen
S1 = 17  # IN1 am Relais
S2 = 27  # IN2 am Relais
S3 = 22  # IN3 am Relais
S4 = 23  # IN4 am Relais

# Setzt die Art der Benennung der GPIO Pins
GPIO.setmode(GPIO.BCM)

# Stellt die GPIO Pins auf Output
GPIO.setup(S1, GPIO.OUT)
GPIO.setup(S2, GPIO.OUT)
GPIO.setup(S3, GPIO.OUT)
GPIO.setup(S4, GPIO.OUT)

# Setzt die GPIO Pins auf die Ausgangsstellung
GPIO.output(S1, 0)  # An
GPIO.output(S2, 1)  # Aus
GPIO.output(S3, 0)  # Aus
GPIO.output(S4, 1)  # An

# Erstellen Sie ein I2C-Bus-Objekt.
i2c = busio.I2C(board.SCL, board.SDA)

# Erstellen Sie ein TSL2591-Objekt.
sensor = adafruit_tsl2591.TSL2591(i2c)

# Definiere welche GPIO Pins was steuern:
klappe = S1
lampe = S2

# Deklaration von Variablen:
klappenzustand = False
tageszeit_anfang = time.time()
tageszeit_ende = time.time()


def alltags_sequenz():
    update_lampen_zustand()
    update_rote_lampen_zustand()
    update_klappenzustand()


def log_lux():
    luxwerte = open("lux_werte", "a")
    luxwerte.write("Uhrzeit:", datetime.datetime.time().now(), "\n"
                   "Luxwert:", sensor.lux, "\n"
                   "Infrarot:", sensor.infrared, "\n"
                   "raw_luminosity", sensor.raw_luminosity, "\n"
                   "-----------------------------------------------------------------")


def update_klappenzustand():
    if daemmerig_oder_heller():
        if klappenzustand:
            return
        setze_tageszeit_anfang()
        setze_klappe(True)
        return

    if not dunkel_oder_dunkler():
        return

    if not klappenzustand:
        return

    setze_tageszeit_ende()
    setze_klappe(False)


def update_lampen_zustand():
    # TODO Lampe an oder ausschalten, je nach Bedingungen
    return


def update_rote_lampen_zustand():
    # TODO Rote Lampe an oder ausschalten, je nach Bedingungen
    return


def daemmerig_oder_heller():
    # TODO Falls es dämmerig oder heller ist → return True, sonst return False
    return True


def dunkel_oder_dunkler():
    # TODO Falls es dunkel oder dunkler ist → return True, sonst return False
    return True


# ändert die Variable klappenzustand, sowie den tatsächlichen Zustand der Klappe via der Raspberry pins
def setze_klappe(p_klappenzustand):
    if p_klappenzustand:
        GPIO.output(klappe, 0)  # 0 = an, also Klappe auf
    else:
        GPIO.output(klappe, 1)  # 1 = aus, also Klappe zu

    global klappenzustand
    klappenzustand = p_klappenzustand


def setze_tageszeit_anfang():
    global tageszeit_anfang
    tageszeit_anfang = time.time()


def setze_tageszeit_ende():
    global tageszeit_ende
    tageszeit_ende = time.time()


while True:
    log_lux()
    time.sleep(300)
