from kafka import KafkaConsumer
import os
import sys
import json
import time
bootstrap_servers = ['kafka:9092']
InputTopicName = 'InputImage'
consumerFile= KafkaConsumer (InputTopicName, group_id = 'group2', bootstrap_servers = bootstrap_servers, api_version = (0,10,0), auto_offset_reset = 'latest')
consumerFile.subscribe(InputTopicName)
for Filename in consumerFile:
    Docker_image=(Filename.value).decode('utf-8')
    print(Docker_image)