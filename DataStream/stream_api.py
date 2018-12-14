import socket
import time
import random

stream = socket.socket()
host = socket.gethostname()
port = 12221
stream.bind((host, port))

stream.listen(5)
connection = None

while True:
  if connection is None:
    print('[Waiting for connection...]')
    connection, addr = stream.accept()
    print('Got connection from', addr)
  else:
    bucket = ""
    bucket += chr(random.randint(65,90))          # bucket first code
    bucket += chr(random.randint(65,90))          # bucket second code
    randomItemNumber = random.randint(1,15)       # number of items in the bucket 
    items = ""
    for i in range (randomItemNumber) :
      item = random.randint(1,300)                # number of different item, range id : 1-300
      items += str(item) + " "
    
    data = {'bucket':bucket,'items':items}
    packet = str(data)
    connection.send(packet.encode())
    time.sleep(0.1)