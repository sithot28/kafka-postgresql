from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="KAFKA_SERVER",
    security_protocol="SSL",
    ssl_cafile="cert/ca-certificate.crt",
    ssl_certfile="cert/user-access-certificate.crt",
    ssl_keyfile="cert/user-access-key.key",
)
