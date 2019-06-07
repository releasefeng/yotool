__author__ = 'Administrator'

import crcmod

#xmodem_crc_func = crcmod.mkCrcFun(0x11021, rev=False, initCrc=0x0000, xorOut=0x0000)
xmodem_crc_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xffff, xorOut=0x0000)
print(hex(xmodem_crc_func('5961D2010001'.decode('hex'))))
