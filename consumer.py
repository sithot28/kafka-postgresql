
from confluent_kafka import Consumer


# Kafka configuration
#KAFKA_SERVER = 'private-db-kafka-sfo3-87231-do-user-1044483-0.c.db.ondigitalocean.com:25080'
KAFKA_SERVER = 'db-kafka-sfo3-87231-do-user-1044483-0.c.db.ondigitalocean.com:25073'
KAFKA_TOPIC = 'csv_data'

# Initialize Kafka Producer
consumer  = Consumer({'bootstrap.servers': KAFKA_SERVER, 'security.protocol': 'SASL_SSL','sasl.username':'doadmin','sasl.mechanism':'PLAIN','sasl.password': 'AVNS__btC7Ck9sPt9DleglEq','ssl.key.location':'/root/source/cert/user-access-key.key','ssl.certificate.location':'/root/source/cert/user-access-certificate.crt','ssl.ca.location':'/root/source/cert/ca-certificate.crt','ssl.endpoint.identification.algorithm': 'none', 'group.id':'salam'})


running = True

def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)
        msg_count = 0
        MIN_COMMIT_COUNT = 10
        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
         #       msg_process(msg)
                print(msg.decode('utf-8'))
                msg_count +=1
                print(msg_count)
                if msg_count % MIN_COMMIT_COUNT == 0:
                    consumer.commit(asynchronous=False)
                    print("commit")
            
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def shutdown():
    running = False


basic_consume_loop(consumer, ['csv_data'])
