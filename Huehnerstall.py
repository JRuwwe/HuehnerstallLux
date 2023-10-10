# Imports können nur am Raspberry funktionieren, Fehlermeldungen am PC normal
import RPi.GPIO as GPIO
import board
import adafruit_tsl2591
import busio

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
