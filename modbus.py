"""
# Modbus Funktionen
# CRC16/Modbus
# Programmiert => Chris Staring
# 2023-12-02, ver 0.1
"""


def modbusCRC(data:str) -> int:
    crc = 0xFFFF
    for n in range(len(data)):
        crc ^= data[n]
        for i in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc