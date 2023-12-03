# -*- coding: utf-8 -*-
"""
# Solis S6 Nulleinspeisung über RS485/Modbus
# mit Shelly 3EM am Einspeisepunkt.
# Codeteile aus verschiedenen Quellen können vorhanden sein. 
# Programmiert => Chris Staring
# 2023-12-02, ver 0.1
"""
#
#
import urllib.request, json 
import time
import I2C_LCD_Driver
import RPi.GPIO as GPIO
import SolisS6_Driver as SolisS6

# GPIO
EINSPEISUNG = 15 #LED für Einspeisung und Nulleinspeisung (grün)
BEZUG = 14 #LED für Bezug (rot)
DISPLAY_TASTER = 17 #Taster für die Umschaltung des Displays auf verschiedene Seiten
GPIO.setmode(GPIO.BCM)
GPIO.setup(EINSPEISUNG, GPIO.OUT)
GPIO.setup(BEZUG, GPIO.OUT)
GPIO.setup(DISPLAY_TASTER, GPIO.IN)

# URL vom Hausverbrauch Shelly
ShellyUrl = "http://192.168.1.47"

# 20x4 LCD über I2C
projectLCD = I2C_LCD_Driver.lcd()
displayMode = 0 # 0 = Übersicht, 1 = WR1 Details, 2 = WR2 Details 
displayCounter = 0 # Nach 60 Schleifen wieder 0 

customLcdIcons = [
        # char(0) - Grid
        [ 0b11111,
	      0b10101,
	      0b11111,
	      0b10101,
	      0b11111,
	      0b10101,
	      0b11111,
	      0b00000 ],

        # char(1) - Stecker
        [ 0b01010,
	      0b01010,
	      0b11111,
	      0b10001,
	      0b10001,
	      0b01110,
	      0b00100,
	      0b00100 ],
        
        # char(2) - Blitz
        [ 0b00010,
	      0b00100,
	      0b01000,
	      0b11111,
	      0b00010,
	      0b00100,
	      0b01000,
	      0b10000 ],
]
projectLCD.lcd_load_custom_chars(customLcdIcons)

# Shelly3EM Hausverbrauch berechnen
def fullHouseConsumption(shellyURL):
    phase1url = ShellyUrl + "/emeter/0"
    phase2url = ShellyUrl + "/emeter/1"
    phase3url = ShellyUrl + "/emeter/2"
    # Phase 1 Gesamtverbrauch
    with urllib.request.urlopen(phase1url) as url:
        data1 = json.load(url)

    # Phase 2 Gesamtverbrauch
    with urllib.request.urlopen(phase2url) as url:
        data2 = json.load(url)
        
    # Phase 3 Gesamtverbrauch
    with urllib.request.urlopen(phase3url) as url:
        data3 = json.load(url)

    phase1power = data1['power']
    phase2power = data2['power']
    phase3power = data3['power']
    return round(float(phase1power) + float(phase2power) + float(phase3power),2)

# Coole Icons vor dem Text auf dem LCD Display
def displayIcons():
    projectLCD.lcd_write(0xC0)
    projectLCD.lcd_write_char(1)
    projectLCD.lcd_write(0x94)
    projectLCD.lcd_write_char(0)
    projectLCD.lcd_write(0xD4)
    projectLCD.lcd_write_char(0)

# Die sagenumwobene Endlosschleife - Beenden mit ^C Keyboard Interrupt
while True:
    # Display Umschaltung
    if (displayCounter == 60):
        displayCounter = 0
        displayMode = 0

    if (GPIO.input(DISPLAY_TASTER) == False):
        if (displayMode == 3):
            displayMode = 0
        displayMode += 1

    # Display mit Shelly Daten füttern und zwischenspeichern
    displayValueConsumption = fullHouseConsumption(ShellyUrl)
    if (displayMode == 0):
        # Normale Ansicht, wenn keine Taste gedrückt wurde
        formattedOutput = "{valueOut:7.2f}"
        formattedInverterOutput = "{valueOut:7}"
        displayIcons()
        projectLCD.lcd_display_string("Nulleinspeisung", 1)
        projectLCD.lcd_display_string_pos("Verbrauch: " + formattedOutput.format(valueOut = displayValueConsumption) + "W", 2, 1)
        projectLCD.lcd_display_string_pos("WR1 1,5kW: " + formattedInverterOutput.format(valueOut = 0) + "W", 3, 1)
        projectLCD.lcd_display_string_pos("WR2 1,5kW: " + formattedInverterOutput.format(valueOut = 0) + "W", 4, 1)
        #print("Verbrauch: %8.2f, Modbus Rückmeldung: %8.2f" % (fullHouseConsumption(ShellyUrl), 0.00))
    if (displayMode == 1): 
        # Details WR 1
        projectLCD.lcd_display_string("Wechselrichter 1", 1)
    if (displayMode == 2):
        # Details WR 2
        projectLCD.lcd_display_string("Wechselrichter 2", 1)

    # LED Party => Einspeisung grün, Ausspeisung Rot
    if (displayValueConsumption <= 0.00):
        GPIO.output(EINSPEISUNG, True)
        GPIO.output(BEZUG, False)
    if (displayValueConsumption > 0.00):
        GPIO.output(EINSPEISUNG, False)
        GPIO.output(BEZUG, True)

    # Abfragen an den Modbus 
    print(SolisS6.totalPower())

    # Antwort aus den Modbus abwarten
    #data_t = ser0.serial.read(8)
    #data += str(data_t)
    displayCounter += 1
    time.sleep(2)