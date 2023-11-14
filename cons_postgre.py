# kafka_consumer.py
import os
from confluent_kafka import Consumer, KafkaError
from db_conn import DatabaseConnection


KAFKA_TOPIC = 'csv_data'
KAFKA_SERVER = os.getenv('KAFKA_SERVER')
KAFKA_PROTOCOL = 'SASL_SSL'
KAFKA_USER = 'doadmin'
KAFKA_PASSWORD = os.getenv('KAFKA_PASSWORD')
KAFKA_MECHANISM = 'PLAIN'

DB_NAME = 'proto'
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = 25060

KAFKA_CONFIG = {
    'bootstrap.servers': KAFKA_SERVER,
    'group.id': 'salam',
    'security.protocol': KAFKA_PROTOCOL,
    'sasl.username': KAFKA_USER,
    'sasl.mechanism': KAFKA_MECHANISM,
    'sasl.password': KAFKA_PASSWORD,
    'ssl.ca.location':'/root/source/cert/ca-certificate.crt',
    'auto.offset.reset': 'earliest'
}

DB_CONFIG = {
    'dbname': DB_NAME,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT
}



def create_consumer(db_conn):
    consumer = Consumer(KAFKA_CONFIG)
    consumer.subscribe([KAFKA_TOPIC])
    n_data = 0
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None or msg.error():
                continue

            data = msg.value().decode('utf-8').split(',')

            try:
                db_conn.insert_into_db(data)
                consumer.commit(message=msg, asynchronous=False)
                n_data += 1
            except Exception as e:
                print(f"Error: {e}")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
    print('processed data ',n_data)

if __name__ == '__main__':
    db_conn = DatabaseConnection(DB_CONFIG)
    try:
        create_consumer(db_conn)
    finally:
        db_conn.close_pool()


