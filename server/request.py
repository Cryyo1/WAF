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
	type=list(elem["Type"].lower())
	if len(type)>1:
		type[0]=type[0].upper()
	elem["Type"]=''.join(type)
	

with open("./data/requests.json","w") as f:
	json.dump(data,f,indent=2)