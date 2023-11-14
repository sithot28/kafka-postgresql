from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO
from confluent_kafka import Producer
import os, csv
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'salamOK'
socketio = SocketIO(app)

# Directory to save uploaded files
UPLOAD_FOLDER = '/root/source/csv'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Kafka configuration
#KAFKA_SERVER = 'private-db-kafka-sfo3-87231-do-user-1044483-0.c.db.ondigitalocean.com:25080'
KAFKA_SERVER = 'db-kafka-sfo3-87231-do-user-1044483-0.c.db.ondigitalocean.com:25073'
KAFKA_TOPIC = 'csv_data'

# Initialize Kafka Producer
producer = Producer({'bootstrap.servers': KAFKA_SERVER, 'security.protocol': 'SASL_SSL','sasl.username':'doadmin','sasl.mechanism':'PLAIN','sasl.password': 'AVNS__btC7Ck9sPt9DleglEq','ssl.key.location':'/root/source/cert/user-access-key.key','ssl.certificate.location':'/root/source/cert/user-access-certificate.crt','ssl.ca.location':'/root/source/cert/ca-certificate.crt','ssl.endpoint.identification.algorithm': 'none'})

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
        socketio.emit('error', {'error': str(err)})
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        
        # Send file to Kafka topic
        n_data = 0
        with open(filename, newline='') as f:
            data = csv.reader(f)
            next(data, None) # skip header
            for row in data:
                msg = ','.join(row)
                producer.produce(KAFKA_TOPIC, msg.encode('utf-8'), callback=delivery_report)
                n_data += 1
        
        producer.flush()
        print('file uploaded and sent to kafka : ',n_data)
        return jsonify({'message': 'File uploaded and sent to Kafka topic'}), 200

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')

