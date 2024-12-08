import pika
from ..utils.es_utils import fetch_document_from_elasticsearch
from chunking import summarize_chunks


def process_document(ch, method, properties, body):
    document_id = body.decode()
    print(f" [x] Received document ID: {document_id}")

    try:
        # Fetch document content from Elasticsearch
        document = fetch_document_from_elasticsearch(document_id)
        document_text = document.get("content", "")
        print(f"[DEBUG] Document content for ID {document_id}: {document_text}")

         # Perform summarization with chunking
        summarized_text = summarize_chunks(document_id, document_text)
        print(f" [x] Summary for document {document_id}: {summarized_text}")


    except Exception as e:
        print(f" [x] Error processing document with ID {document_id}: {str(e)}")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue from which to consume
    channel.queue_declare(queue='document_queue', durable=True)

    # Set up the consumer
    channel.basic_consume(queue='document_queue', on_message_callback=process_document)

    print(' [*] Waiting for documents. To exit press CTRL+C')
    channel.start_consuming()

consume_from_queue()
