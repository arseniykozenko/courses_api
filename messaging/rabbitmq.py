"""rabbitmq config"""
import os
import pika
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")


credentials = pika.PlainCredentials(
    username=RABBITMQ_USER,
    password=RABBITMQ_PASS
)

parameters = pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    credentials=credentials,
    heartbeat=600,
    blocked_connection_timeout=300
)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
