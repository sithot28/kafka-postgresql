from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="db-kafka-sfo3-87231-do-user-1044483-0.c.db.ondigitalocean.com:25073",
    security_protocol="SSL",
    ssl_cafile="cert/ca-certificate.crt",
    ssl_certfile="cert/user-access-certificate.crt",
    ssl_keyfile="cert/user-access-key.key",
)
