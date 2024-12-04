from confluent_kafka import Consumer, KafkaException, KafkaError
import sys

KAFKA_CONFIG = {
    'bootstrap.servers': 'your_kafka_server',
    'group.id': 'your_group_id',
    'auto.offset.reset': 'earliest'
}

def create_consumer():

    KAFKA_SERVER = 'KAFKA_SERVER'
    KAFKA_TOPIC = 'csv_data'

    # Initialize Kafka Consumer
    consumer  = Consumer()


    def on_assign(consumer, partitions):
        print('Assignment:', partitions)

    # Subscribe to the topic
    consumer.subscribe([KAFKA_TOPIC], on_assign=on_assign)


    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            print('Received message: {}'.format(msg.value().decode('utf-8')))

    except KeyboardInterrupt:
        pass
    except KafkaException as e:
        print(e)
    finally:
        consumer.close()

if __name__ == '__main__':
    create_consumer()

