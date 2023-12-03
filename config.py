"""
# PiHat Dual RS485 von Waveshare
# Konfiguration vom HAT
# Programmiert => Chris Staring
# 2023-12-02, ver 0.1
"""

import serial
import RPi.GPIO as GPIO

TXDEN_1 = 27
TXDEN_2 = 22

# dev = "/dev/ttySC0"

class config(object):
    def __init__(ser, Baudrate = 9600, dev = "/dev/ttyS0"):
        print (dev)
        ser.dev = dev
        ser.serial = serial.Serial(ser.dev, Baudrate)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TXDEN_1, GPIO.OUT)
        GPIO.setup(TXDEN_2, GPIO.OUT)

        GPIO.output(TXDEN_1, GPIO.HIGH)
        GPIO.output(TXDEN_2, GPIO.HIGH)
        
    def Uart_Set_Baudrate(ser, Baudrate):
         ser.serial = serial.Serial(ser.dev, Baudrate)
    
    
        
         