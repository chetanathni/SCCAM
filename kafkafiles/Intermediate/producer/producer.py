from kafka import KafkaConsumer
from kafka import KafkaProducer
from pymongo import MongoClient
import threading
#from docker import client
import docker
import queue
import os
import sys
import json
import time
from json import loads
#client = docker.from_env()
#mongodb connection
#username = os.environ['MONGO_INITDB_ROOT_USERNAME']
#password = os.environ['MONGO_INITDB_ROOT_PASSWORD']
username='admin'
password='password'
#intermediate connection
db_server='mongodb:27017'
conn = MongoClient(db_server, username=username, password=password)
db = conn.database
collection = db.all_data
cursor = collection.find()
'''
#backend connection
db_server_backend='35.239.220.105:27017'
conn_backend = MongoClient(db_server_backend, username=username, password=password)
db_backend = conn_backend.database
collection_backend = db_backend.filtered_data
cursor2 = collection_backend.find()
'''
#kafka connections
bootstrap_servers = ['kafka:9092']
sending_server = ['kafka:9092']
GetArea=''
GetCity=''
'''
pipeline = [
  {
       "$group":
         {
           "_id": "$area",
           "avgQuantity": { "$avg": "$ppm" }
         }
     }
]
cursor = collection.aggregate(pipeline)
for i in cursor:
        print(i)
'''
#act as consumer to get edge data from all VMs sending to a particular topic and set it to variable data
def GetFunc(fname):
        InputTopicName = 'functionName'
        consumerFunc= KafkaConsumer (InputTopicName, group_id = 'group2', bootstrap_servers = bootstrap_servers, api_version = (0,10,0), 
auto_offset_reset = 'latest')
        consumerFunc.subscribe(InputTopicName)
        for Funcname in consumerFunc:
                Function_name=(Funcname.value).decode('utf-8')
                fname.put(Function_name)
                pipeline = [{"$group":{"_id": "$area","val": { "${}".format(Function_name): "$ppm" }}}]
                cursor = collection.aggregate(pipeline)
                #sval.put(cursor[0]['value'])
                print(list(cursor))
def GetOption(q,client):
        OptionTopicName = 'OptionName'
        #global client
        OptionConsumer= KafkaConsumer (OptionTopicName, group_id = 'group1', bootstrap_servers = bootstrap_servers, api_version = (0,10,0
), auto_offset_reset = 'latest')
        OptionConsumer.subscribe(OptionTopicName)
        for OptionName in OptionConsumer:
                Option=(OptionName.value).decode('utf-8')
                print(Option)
                if (Option!='None' and Option!='NOne' and Option!='flaski/flaski'):
                     for line in client.pull(Option,stream=True,decode=True):
                             print(json.dumps(line, indent=4))
                     op = client.create_container(Option)
                     os.system("docker run "+Option)
                     #print(client.top(op,ps_args=None))
                     #print(client.start(container=op['Id']))
                     #x=client.images.pull(Option)
                     #client.containers.run(Option,"echo received")
def GetFile(r):
        InputTopicName = 'InputImage'
        consumerFile= KafkaConsumer (InputTopicName, group_id = 'group1', bootstrap_servers = bootstrap_servers, api_version = (0,10,0), 
auto_offset_reset = 'latest')
        consumerFile.subscribe(InputTopicName)
        for Filename in consumerFile:
                Docker_image=(Filename.value).decode('utf-8')
                r.put(Docker_image)
                print(Docker_image)
def SendFile(r):
        InputTopicName = 'FileName'
        producer = KafkaProducer(bootstrap_servers = sending_server, api_version=(0,10,0),value_serializer = lambda v: json.dumps(v).encode('utf-8'))
        while(1):
                Dockerfile=r.get()
                producer.send(InputTopicName,Dockerfile)
                producer.flush()
def GetData(q):
        #global SentCity,SentArea,SentData
        DataTopicName = 'sample'
        consumerData = KafkaConsumer (DataTopicName, group_id = 'test-consumer-group',bootstrap_servers = bootstrap_servers,api_version=(
0,10,0),auto_offset_reset = 'latest',value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        for message in consumerData:
                x=message.value
                #print(collection.insert(x))    #send all the data to intermediate DB
                area=x["area"].split("-")
                SentCity=area[0]
                SentArea=area[1]
                date=x["date"]
                time=x["time"]
                ppm=x["ppm"]
                CPU=x["CPU"]
                total_RAM=x["total_RAM"]
                used_RAM=x["used_RAM"]
                percent_used=x["percent_used"]
                datalist=[ppm,CPU,total_RAM,used_RAM,percent_used]
                #print(datalist)
                q.put(datalist)
                """   if(GetCity==SentCity and GetArea==SentArea):
                        print("Match found")
                        q.put(datalist) 
                        print("Data forwarded to backend ")
                        print(datalist)
                """
#push to db
#act as consumer to get location from backend
def GetLoc():
        global GetCity,GetArea
        LocationTopicName = 'LocationReq'
        consumerLocn= KafkaConsumer (LocationTopicName, group_id = 'group1', bootstrap_servers = bootstrap_servers, api_version = (0,10,0
), auto_offset_reset = 'latest')
        consumerLocn.subscribe(LocationTopicName)
        for Locmessage in consumerLocn:
                loc=(Locmessage.value)
                locList=loc.decode('utf-8').split(' ')
                GetArea=locList[1]
                GetCity=locList[0]
                print("Got these "+GetCity+" "+GetArea)
def filters(q):
                sendingTopic = 'filtered'
                producer = KafkaProducer(bootstrap_servers = sending_server, api_version=(0,10,0),value_serializer = lambda v: json.dumps
(v).encode('utf-8'))

                while(1):
                        SentData=q.get()
                        #collection_backend.insert(SentData)   #send filtered data to DB {need to send the dict}
                        producer.send(sendingTopic,SentData)
                        producer.flush()
if __name__ == "__main__":
    # creating thread
        q = queue.Queue()
        r = queue.Queue()
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        #client = client(base_url='unix://var/run/docker.sock')
        fname = queue.Queue()
        t1 = threading.Thread(target=GetData ,args=(q,))
        t2 = threading.Thread(target=filters ,args=(q,))
        t3 = threading.Thread(target=GetLoc)
        t4 = threading.Thread(target=GetOption ,args=(q,client,))
        t5 = threading.Thread(target=GetFunc ,args=(fname,))
        t1.start()
        t2.start()
        #t3.start()
        t4.start()
        #t5.start()
