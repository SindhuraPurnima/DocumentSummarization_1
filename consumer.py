import pika
from transformers import pipeline

summarizer = pipeline("summarization")

def process_document(ch, method, properties, body):
    document_text = body.decode()
    print(f" [x] Received document: {document_text}")
    # You can integrate your summarization logic here
    summarized_document = summarizer(document_text, max_length=150, min_length=30, do_sample=False)
    print(f" [x] Summarized document: {summarized_document}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue from which to consume
    channel.queue_declare(queue='document_queue')

    # Set up the consumer
    channel.basic_consume(queue='document_queue', on_message_callback=process_document)

    print(' [*] Waiting for documents. To exit press CTRL+C')
    channel.start_consuming()

consume_from_queue()
