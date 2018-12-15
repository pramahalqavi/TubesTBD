import socket
import time
import random
import datetime

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
    basket = ""
    basket += chr(random.randint(65,90))          # basket first code
    basket += chr(random.randint(65,90))          # basket second code
    randomItemNumber = random.randint(1,10)       # number of items in the basket 
    items = []
    for i in range (randomItemNumber) :
      item = random.randint(1,100)                # number of different item, range id : 1-100
      items.append(item)
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    
    data = {'basket':basket,'items':items,'time':timestamp}
    packet = str(data)
    connection.send(packet.encode())
    time.sleep(0.5)