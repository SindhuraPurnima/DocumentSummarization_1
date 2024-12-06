import pika
from transformers import pipeline
from ..utils.es_utils import fetch_document_from_elasticsearch

# Initialize the summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def process_document(ch, method, properties, body):
    document_id = body.decode()
    print(f" [x] Received document ID: {document_id}")

    try:
        # Fetch document content from Elasticsearch
        document = fetch_document_from_elasticsearch(document_id)
        document_text = document.get("content", "")

        # Perform summarization
        if document_text:
            print(" [x] Performing summarization...")
            summary = summarizer(document_text, max_length=150, min_length=30, do_sample=False)
            summarized_text = summary[0]["summary_text"]

            print(f" [x] Summary for document {document_id}: {summarized_text}")

            # Save or log the summarized text (can be stored back in Elasticsearch or printed)
            # For now, we just print the summary
        else:
            print(f" [x] Document content is empty for ID: {document_id}")

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
