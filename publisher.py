import pika

def send_to_queue(document_text):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='document_queue')

    # Send document to the queue
    channel.basic_publish(exchange='',
                          routing_key='document_queue',
                          body=document_text)
    print(" [x] Sent document to queue")
    connection.close()

# Example usage:
document = "This is a sample document for summarization."
send_to_queue(document)
