"""
This program sends a single message to the queue

June 21, 2022
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# We're connected now, to a broker on the local machine - hence the localhost.
# If we wanted to connect to a broker on a different machine we'd simply specify its name or IP address here.

channel.queue_declare(queue="hello")

channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
print(" [x] Sent 'Hello World!'")

connection.close()

