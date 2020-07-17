#imports and universal constants
from kafka import KafkaConsumer
from kafka import KafkaProducer
from pymongo import MongoClient
import threading
import queue
import os
import sys
import json
import time
from json import loads

#mongodb connection

username = os.environ['MONGO_INITDB_ROOT_USERNAME']
password = os.environ['MONGO_INITDB_ROOT_PASSWORD']
#intermediate connection
db_server_intermediate='mongodb:27017'
conn_intermediate = MongoClient(db_server_intermediate, username=username, password=password)
db_intermediate = conn_intermediate.database
collection_intermediate = db_intermediate.all_data
cursor1 = collection_intermediate.find()

#backend connection
db_server_backend='<backend IP >:27017'
conn_backend = MongoClient(db_server_backend, username=username, password=password)
db_backend = conn_backend.database
collection_backend = db_backend.filtered_data
cursor2 = collection_backend.find()

#kafka connections
bootstrap_servers = ['kafka:9092']
sending_server = ['<backend IP>:9092']
GetArea=''
GetCity=''

#act as consumer to get anantha's data from all VMs sending to a particular topic and set it to variable data


def GetFile(r):
        InputTopicName = 'InputImage'
        consumerFile= KafkaConsumer (InputTopicName, group_id = 'group1', bootstrap_servers = bootstrap_servers, api_version = (0,10,0), auto_offset_reset = 'latest')
        consumerFile.subscribe(InputTopicName)
        for Filename in consumerFile:
                Docker_image=(Filename.value).decode('utf-8')
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
        consumerData = KafkaConsumer (DataTopicName, group_id = 'test-consumer-group',bootstrap_servers = bootstrap_servers,api_version=(0,10,0),auto_offset_reset = 'latest',value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        for message in consumerData:
                collection_intermediate.insert(message.value)    #send all the data to intermediate DB
                x=message.value
                for city,data1 in x.items():
                        for area,data2 in data1.items():
                                for date,data3 in data2.items():
                                        for timey,datalist in data3.items():
                                                SentCity=city
                                                SentArea=area
                                                print("Data received from edge ")
                                                print(datalist)
                                                if(GetCity==SentCity and GetArea==SentArea):
                                                        print("Match found")
                                                        q.put(datalist) 
                                                        print("Data forwarded to backend ")
                                                        print(datalist)
#push to db

#act as consumer to get location from backend
def GetLoc():
        global GetCity,GetArea
        LocationTopicName = 'LocationReq'
        consumerLocn= KafkaConsumer (LocationTopicName, group_id = 'group1', bootstrap_servers = bootstrap_servers, api_version = (0,10,0), auto_offset_reset = 'latest')
        consumerLocn.subscribe(LocationTopicName)
        for Locmessage in consumerLocn:
                loc=(Locmessage.value)
                locList=loc.decode('utf-8').split(' ')
                GetArea=locList[1]
                GetCity=locList[0]
                print("Got these "+GetCity+" "+GetArea)
def filters(q):
                sendingTopic = 'filtered'
                while(1):
                        producer = KafkaProducer(bootstrap_servers = sending_server, api_version=(0,10,0),value_serializer = lambda v: json.dumps(v).encode('utf-8'))
                        SentData=q.get()
                        #collection_backend.insert(SentData)   #send filtered data to DB {need to send the dict}
                        producer.send(sendingTopic,SentData)
                        producer.flush()
                        print("Sent Data is ")
                        print(SentData)
                        print("\n\n\n")
if __name__ == "__main__":
    # creating thread
        q = queue.Queue()
        r = queue.Queue()
        t1 = threading.Thread(target=GetData ,args=(q,))
        t2 = threading.Thread(target=filters ,args=(q,))
        t3 = threading.Thread(target=GetLoc)
        t4 = threading.Thread(target=GetFile ,args=(r,))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

