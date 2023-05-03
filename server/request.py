import json 
import uuid
import random
import time
from datetime import datetime

def randomDate(start, end):
    frmt = '%d-%m-%Y %H:%M:%S'

    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))

    ptime = stime + random.random() * (etime - stime)
    dt = datetime.fromtimestamp(time.mktime(time.localtime(ptime)))
    return dt


with open("./data/requests.json","r") as f:
	data=json.loads(f.read())

for elem in data:
	random_datetime = randomDate("20-01-2023 8:30:00", "23-04-2023 16:50:34")
	elem["Date time"]=str(random_datetime)
	elem["id"]=str(uuid.uuid1()).split('-')[0]

with open("./data/requests.json","w") as f:
	json.dump(data,f,indent=2)