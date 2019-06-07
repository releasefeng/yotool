import serial
import crcmod

Ygcboardev=serial.Serial(sernum,rate,timeout=10)
mess='59ee80171400000000000000000000000000000000000000000040a1345347'
Ygcboardev.write(tocksend)
while True:
    result=''
    recvHead=Ygcboardev.read()
    hexHead = ord(recvHead)
    frameHead = '%02x'%hexHead
    if frameHead == '59':
        soflag=1
        result+=frameHead
        recvbinbid=Ygcboardev.read()
        hexbid = ord(recvbinbid)
        recvbid = '%02x'%hexbid
        result+=recvbid
        recvbincmd=Ygcboardev.read()
        hexcmd = ord(recvbincmd)
        recvcmd = '%02x'%hexcmd
        result+=recvcmd
        recvbinlen=Ygcboardev.read()
        hexlen = ord(recvbinlen)
        recvlen = '%02x'%hexlen
        result+=recvlen
        length=int(recvlen,16)
        for i in range(0,length+4):
            message=Ygcboardev.read()
            hvol = ord(message)
            hhex = '%02x'%hvol
            result += hhex
    print(result)