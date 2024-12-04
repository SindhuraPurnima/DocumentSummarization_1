import pika

def send_to_queue(queue_name: str, message: str):
    """
    Send a message to the specified RabbitMQ queue.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue="document_queue",durable=True)

        # Publish the message
        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        print(f" [x] Sent message to queue: {queue_name}")

        connection.close()
    except Exception as e:
        print(f"Error while sending to RabbitMQ: {str(e)}")
        raise
