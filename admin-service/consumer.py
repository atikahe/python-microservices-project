import pika
import os

RABBIT_MQ_SERVER = os.getenv('RABBIT_MQ_SERVER')
RABBIT_MQ_USER = os.getenv('RABBIT_MQ_USER')
RABBIT_MQ_PASS = os.getenv('RABBIT_MQ_PASS')
RABBIT_MQ_PROTOCOL = os.getenv('RABBIT_MQ_PROTOCOL')

# Connect to CloudAMQP
params = pika.URLParameters(f'{RABBIT_MQ_PROTOCOL}://{RABBIT_MQ_USER}:{RABBIT_MQ_PASS}@{RABBIT_MQ_SERVER}/{RABBIT_MQ_USER}')
connection = pika.BlockingConnection(params)
 
# Create channel
channel = connection.channel()

# Declare queue
channel.queue_declare(queue='admin')

# Create callback function
def callback(channel, method, properties, body):
    print('Receiving in admin')
    print(body)

# Initiate consumer
channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

# Will consume data and run callback in every consume
print('Started consuming')
channel.start_consuming()

# Close connection
channel.close()