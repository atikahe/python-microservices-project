import pika
import json
import os

from models import db, Product

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
channel.queue_declare(queue='main')

# Declare callback
def callback(channel, method, properties, body):
    print('Receiving in main')
    data = json.loads(body)
    print(data)
    print(properties.content_type)
    
    if properties.content_type == 'product_created':
        product = Product(id=data.get('id'), title=data.get('title'), image=data.get('image'))
        db.session.add(product)
        db.session.commit()
        print('Product Created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Product Updated')
    
    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        print('Product Deleted')

# Initiate consumer
channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

# Start consuming
print('Started consuming')
channel.start_consuming()

# Close connection
channel.close()