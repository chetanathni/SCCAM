from kafka import KafkaConsumer

bootstrap_servers=['kafka:9092']

TopicName ='InputImage'
consumer= KafkaConsumer (TopicName, group_id = 'group2', bootstrap_servers = bootstrap_servers, api_version = (0,10,0), auto_offset_reset = 'latest')
consumer.subscribe(TopicName)

for message in consumer:
	print(message.value)



	