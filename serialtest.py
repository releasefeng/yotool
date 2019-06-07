import serial

serDevice=serial.Serial('COM3',9600,timeout=10)

#serDevice.write("\x57".encode('utf-8'))
serDevice.write("\x49\x00\x00\x00\x00\x57".encode('utf-8'))
#serDevice.write("\x57")
