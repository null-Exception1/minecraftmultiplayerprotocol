import socket
import binascii
import struct
d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
d.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
d.bind(("localhost",25565))
d.listen()

cs, addr = d.accept()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = socket.gethostbyname('chiweenie.aternos.host')
s.connect((ip,50853))
#
s.settimeout(0.2)
cs.settimeout(0.2)

ping = b'\x1b'
while True:
    try:
        try:
            recved = cs.recv(4096)
            length = recved[0]

            if length == 27: # pos
                #print("pos",binascii.hexlify(recved))
                
                x = binascii.hexlify(recved)[6:22]
                y = binascii.hexlify(recved)[22:38]
                z = binascii.hexlify(recved)[38:54]

                x = struct.unpack('>d',binascii.unhexlify(x)) # (IEE 754 double)
                y = struct.unpack('>d',binascii.unhexlify(y)) # (IEE 754 double)
                z = struct.unpack('>d',binascii.unhexlify(z)) # (IEE 754 double)
                
                #print("pos",x,y,z)
                #pass
            
            elif length == 11: # rot

                #print("rot",binascii.hexlify(recved))
                yaw = binascii.hexlify(recved)[6:14]
                pitch = binascii.hexlify(recved)[14:22]

                yaw = struct.unpack('>f',binascii.unhexlify(yaw)) # (IEEE 754 floating point number)
                pitch = struct.unpack('>f',binascii.unhexlify(pitch)) # (IEEE 754 floating point number)

                #print('rot', yaw, pitch)

            elif length == 35: # pos + rot
                #print("rot",binascii.hexlify(recved))
                x = binascii.hexlify(recved)[6:22]
                y = binascii.hexlify(recved)[22:38]
                z = binascii.hexlify(recved)[38:54]

                x = struct.unpack('>d',binascii.unhexlify(x)) # (IEE 754 double)
                y = struct.unpack('>d',binascii.unhexlify(y)) # (IEE 754 double)
                z = struct.unpack('>d',binascii.unhexlify(z)) # (IEE 754 double)
                
                yaw = binascii.hexlify(recved)[54:62]
                pitch = binascii.hexlify(recved)[62:70]

                yaw = struct.unpack('>f',binascii.unhexlify(yaw)) # (IEEE 754 floating point number)
                pitch = struct.unpack('>f',binascii.unhexlify(pitch)) # (IEEE 754 floating point number)

                #print('pos + rot', x ,y, z, yaw, pitch)
            elif binascii.hexlify(recved) == b'03002f00':
                #print('hits something')
                pass
            elif binascii.hexlify(recved).startswith(b'0600'):
                #print("sprint",binascii.hexlify(recved))
                if binascii.hexlify(recved).endswith(b'300'):
                    #print('sprint start')
                    recved = binascii.unhexlify('06001ee0290300')
                    pass
                if binascii.hexlify(recved).endswith(b'400'):
                    #print('sprint end')
                    recved = binascii.unhexlify('06001ee0290400')
                    pass
                pass
            elif binascii.hexlify(recved).startswith(b'04002800'):
                #print("switch hotbar",recved[-1])
                pass
            else:
                print("client ",binascii.hexlify(recved))
            s.send(recved)
        except socket.timeout:
            pass
        try:
            recved = s.recv(4096)
            print("server",binascii.hexlify(recved[:32]))

            cs.send(recved)
        except socket.timeout:
            pass
    except KeyboardInterrupt:
        s.close()
        cs.close()
        break
