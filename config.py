"""
Compiled, mashed and generally mutilated 2023 by Chris Staring
Made available under GNU GENERAL PUBLIC LICENSE
# PiHat Dual RS485
# added bits and pieces from various sources
# By Chris Staring
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
        
    def Uart_SendByte(ser, value): 
        ser.serial.write(value.encode('ascii')) 
    
    def Uart_SendString(ser, value): 
        ser.serial.write(value.encode('ascii'))

    def Uart_ReceiveByte(ser): 
        return ser.serial.read(1).decode("utf-8")

    def Uart_ReceiveString(ser, value): 
        data = ser.serial.read(value)
        return data.decode("utf-8")
        
    def Uart_Set_Baudrate(ser, Baudrate):
         ser.serial = serial.Serial(ser.dev, Baudrate)
    
    
        
         