import socket
import time
import random

s = socket.socket()
host = socket.gethostname()
port = 12221
s.bind((host, port))

s.listen(5)
c = None

while True:
   if c is None:
       print('[Waiting for connection...]')
       c, addr = s.accept()
       print('Got connection from', addr)
   else:
       k = ""
       k += chr(random.randint(65,90))
       k += chr(random.randint(65,90))
       v = random.randint(1,9999)
       kv = {'key':k,'value':v}
       q = str(kv)
       c.send(q.encode())
       time.sleep(1)