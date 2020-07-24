import datetime
import time
import random
import string
import json
from kafka import KafkaProducer
import psutil
bootstrap_servers = ['kafka:9092']
producer = KafkaProducer(bootstrap_servers = bootstrap_servers,api_version=(0,10,0),value_serializer=lambda v: json.dumps(v).encode('utf-8'))
place = 'bangalore-north'


def get_size(bytes, suffix="B"):

    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
        

while(1):
    now = datetime.datetime.now()
    day = str(now.day)
    month = str(now.month)
    year = str(now.year)
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    CPU = psutil.cpu_percent()
    A = psutil.virtual_memory()
    total = get_size(A.total)
    used = get_size(A.used)
    percent = A.percent
    area = random.choice(areas)
    date = day+'-'+month+'-'+year
    timey = hour+':'+minute+':'+second
    ppm = (random.random())*1000
    #data = {place: {area:{date: {timey:[ppm,CPU,total,used,percent]}}}}
    #data = [ppm,CPU,total,used,percent]
    data = {'area':place,'date':date,'time':timey,'ppm':ppm,'CPU':CPU,'total_RAM':total,'used_RAM':used,'percent_used':percent}
    producer.send('sample', data)
    producer.flush()
    time.sleep(2)
