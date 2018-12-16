import socket
import threading
import time
import random
import datetime
from efficient_apriori import apriori

stream = socket.socket()
host = socket.gethostname()
port = 12221

stream.connect((host, port))
print('Connected to', host)

dataList = []
itemCount = []
dataToLook = [1,2]
expireSecondFromNow = 300		# data will be ignored if already been there for 300s
for i in range(0,11): itemCount.append(0)

def listen():
	while True:
		message = stream.recv(1024)
		if not message:
			break
		packet = message.decode('ascii')
		data = eval(packet)
		dataList.append(data)
		print(data)
		for x in data['items']: itemCount[x] += 1

def checkDataExpiry(expiredTimeInSecond) :
	while True :
		time.sleep(expiredTimeInSecond)
		expiredTime = datetime.datetime.now() - datetime.timedelta(seconds=expiredTimeInSecond)
		checkExpiry = False
		while (not(checkExpiry) and (len(dataList) != 0)) :
			if (datetime.datetime.strptime(dataList[0]['time'], '%Y-%m-%d %H:%M:%S') < expiredTime) :
				data = dataList.pop(0)
				for x in data['items']: itemCount[x] -= 1
			else :
				checkExpiry = True

def sampling(n,nbucket,delay,loop):
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
		if n <= len(num):
			pick = []
			for i in range(n):
				for j in buckets[i]: pick.append(j)
		else: pick = buckets[random.choice(num)]
		print("Sampling",n,"/",nbucket,"of",len(tempDataList),"data:",pick)
		print()

def bucketHash(data,done,buckets):
	num = [i for i, x in enumerate(done) if x == False]
	if len(num) == 0:
		for i in range(len(buckets)): done[i] = False
		num = [x for x in range(10)]
	bucket_no = random.choice(num)
	buckets[bucket_no].append(data)
	done[bucket_no] = True

def filtering(containData,delay,loop):
	for l in range(loop):
		time.sleep(delay)
		tempDataList = dataList
		filtered = []
		for x in tempDataList:
			if all(elem in x['items']  for elem in containData): filtered.append(x)
		print("Filtered data containing",containData,":\n",filtered)
		print()

def countDistinct(delay,loop):
	for l in range(loop):
		time.sleep(delay)
		tempItemCount = itemCount
		print("Count Distinct Item:")
		for i in range(1,len(tempItemCount)): print(i,":",tempItemCount[i]),
		print()


def countItemSets(support,delay,loop):
	for l in range(loop):
		time.sleep(delay)
		print("Counting Itemsets...")
		tempDataList = dataList
		transactions = [x['items'] for x in tempDataList]
		itemsets, rules = apriori(transactions, min_support=support,  min_confidence=1)
		print("Count Itemsets (Min Support",support,"):")
		print(itemsets)
		print()

try:
	threading.Thread(target=listen).start()
	threading.Thread(target=checkDataExpiry, args=[expireSecondFromNow]).start()
	threading.Thread(target=sampling, args=(2,10,10,1)).start()
	threading.Thread(target=filtering, args=(dataToLook,4,1)).start()
	threading.Thread(target=countDistinct, args=(6,1)).start()
	threading.Thread(target=countItemSets, args=(0.2,8,1)).start()

except:
	print("Error: unable to start thread")

# time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timetuple())