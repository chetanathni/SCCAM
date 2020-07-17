from kafka import KafkaConsumer
from kafka import KafkaProducer
from pymongo import MongoClient 
import json
bootstrap_servers=['kafka:9092']
db_server='mongodb:27017'
topicName ='sample'

consumer = KafkaConsumer (topicName, group_id = 'test-consumer-group',bootstrap_servers = bootstrap_servers,api_version=(0,10,0),auto_offset_reset = 'latest',value_deserializer=lambda m: json.loads(m.decode('utf-8')))
consumer.subscribe(topicName)

conn = MongoClient(db_server, 27017)
db = conn.database 
collection = db.all_data 
cursor = collection.find() 


for message in consumer:
	print(message.value)
	collection.insert_one(message.value) 

#for record in cursor: 
#    print(record) 

