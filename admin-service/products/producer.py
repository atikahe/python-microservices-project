import pika
import json

# Initialize connection
params = pika.URLParameters('amqps://sxtjyces:iKNQG-SFEXRAz78RWjXdY5mcgh4njEJO@snake.rmq2.cloudamqp.com/sxtjyces')
connection = pika.BlockingConnection(params)
 
# Create channel
channel = connection.channel()

# Function to produce event
def publish(method, body):
    # Declare properties
    properties = pika.BasicProperties(method)
    # Publish message
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)