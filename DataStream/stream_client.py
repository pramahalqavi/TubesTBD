import socket
import threading
import time
import random

stream = socket.socket()
host = socket.gethostname()
port = 12221

stream.connect((host, port))
print('Connected to', host)

dataList = []

def listen():
	while True:
		message = stream.recv(1024)
		if not message:
			break
		packet = message.decode('ascii')
		data = eval(packet)
		dataList.append(data)
		print(data)

def sampling(nbucket,delay,loop):
	for l in range(loop):
		time.sleep(delay)
		tempDataList = dataList
		done = []
		buckets = []
		for i in range(nbucket): 
			done.append(False)
			buckets.append([])
		for x in tempDataList:
			bucketHash(x,done,buckets)
		num = [i for i, x in enumerate(buckets) if len(x) > 0]
		pick = random.choice(num)
		print("Sampling 1 /",nbucket,"of",len(tempDataList),"data:",buckets[pick])
		print()

def bucketHash(data,done,buckets):
	num = [i for i, x in enumerate(done) if x == False]
	if len(num) == 0:
		for i in range(len(buckets)): done[i] = False
		num = [x for x in range(10)]
	bucket_no = random.choice(num)
	buckets[bucket_no].append(data)
	done[bucket_no] = True

try:
	threading.Thread(target=listen).start()
	threading.Thread(target=sampling, args=(10,3,10)).start()

except:
	print("Error: unable to start thread")

