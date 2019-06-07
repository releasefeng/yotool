from PyCRC.CRC16 import CRC16

def calCRC16(input):
    CRCResult=CRC16().calculate(input)
    return CRCResult

input=b'\x59\x47\x00\x00\x00'
result=hex(calCRC16(input))
print(result)