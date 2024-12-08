from transformers import pipeline

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def chunk_document(document_text, chunk_size=500):
    """
    Splits the document text into smaller chunks of a specified size (in words).
    """
    words = document_text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

def summarize_chunks(document_id, document_text, chunk_size=500, max_length=150):
    """
    Summarizes a document by breaking it into chunks and summarizing each chunk.
    """
    print(f"[DEBUG] Starting summarization for document ID {document_id}...")
    chunks = chunk_document(document_text, chunk_size=chunk_size)
    summaries = []
    
    for idx, chunk in enumerate(chunks):
        print(f"[DEBUG] Summarizing chunk {idx + 1}/{len(chunks)}...")
        try:
            summarized_chunk = summarizer(chunk, truncation=True, max_length=max_length)[0]['summary_text']
            summaries.append(summarized_chunk)
            print(f"[DEBUG] Chunk {idx + 1} Summary: {summarized_chunk}")
        except Exception as e:
            print(f"[!] Error during summarization for chunk {idx + 1}: {e}")
    
    # Combine all chunk summaries into a final summary
    final_summary = " ".join(summaries)
    print(f"[DEBUG] Final Summary for document ID {document_id}: {final_summary}")
    return final_summary
