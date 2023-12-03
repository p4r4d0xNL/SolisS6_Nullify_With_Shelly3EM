"""
# Solis S6 Modbus
# Programmiert => Chris Staring
# 2023-12-02, ver 0.1
"""

import modbus
import RPi.GPIO as GPIO
import serial
import config as rs485
import time

# RS485
TXDEN_1 = 27
TXDEN_2 = 22
ser0 = rs485.config(dev = "/dev/ttySC0")

def totalPower() -> int:
    #msg = bytes.fromhex("01060beb2710") # Kein korrekter CRC16/Modbus... -> 100% Leistung
    inverterW = 0
    msg = bytes.fromhex("01040bbc0002")
    crc =  modbus.modbusCRC(msg)
    crcLittle = crc.to_bytes(2, byteorder="little")
    msg += crcLittle
    GPIO.output(TXDEN_1, GPIO.LOW)  
    ser0.serial.write(msg)
    GPIO.output(TXDEN_1, GPIO.HIGH)
    time.sleep(0.005)
    #dataArray = ser0.serial.read(10) # Ergebnis lesen :-). Keine RS485! 
    dataArray = [b'\01', b'\04', b'\02', b'\00', b'\00']
    if (dataArray[0] == b'\x01'):
        if (dataArray[1] == b'\x04'):
            #inverterW = dataArray[3] + dataArray[4] # Byte in Hex!!!
            inverterW = 0 # Hex in Dezimal!
    return inverterW

def test() -> bytes:
    msg = bytes.fromhex("01040bb70001") # Vollkommen korrekt!
    crc =  modbus.modbusCRC(msg)
    crcLittle = crc.to_bytes(2, byteorder="little")
    msg += crcLittle
    return msg
