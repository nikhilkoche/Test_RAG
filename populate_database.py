import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain_chroma import Chroma
from memory_profiler import memory_usage
# from populate_database import count_pdf_documents,number_of_pages
import os
import time
from tqdm import tqdm

CHROMA_PATH = "chroma"
DATA_PATH = "data"




def main():

    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("🗑️ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def load_documents():
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document]):
    
    mem_start= memory_usage()[0]
    start_time = time.time()
    number_of_documents,total_size_docs = count_pdf_documents(DATA_PATH)
    num_pages = number_of_pages()

    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    # if len(new_chunks):
    #     print(f"👉 Adding new documents: {len(new_chunks)}")
    #     new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
    #     db.add_documents(new_chunks, ids=new_chunk_ids)
        
    # else:
    #     print("✅ No new documents to add")

    

    if len(new_chunks) > 0:
        print(f"📃Adding new documents: {len(new_chunks)}")
        
        # Create a tqdm progress bar
        with tqdm(total=len(new_chunks), desc="Adding Documents", unit="document") as pbar:
            for chunk in new_chunks:
                chunk_id = chunk.metadata["id"]
                db.add_documents([chunk], ids=[chunk_id])  # Add one document at a time
                pbar.update(1)  # Update the progress bar after each document is added
    else:
        print("✅ No new documents to add")
    
    end_time=time.time()
    mem_end= memory_usage()[0]
    print(f"{'Total Number of Documents':<30}: {number_of_documents}")
    print(f"{'Total Number of Pages':<30}: {num_pages}")
    print(f"{'Total size of documents':<30}: {round(total_size_docs,2)}{' MiB'}")
    print(f"{'Memory Usage':<30}: {round(mem_end-mem_start,2)}{' MiB'}")
    print(f"{'Latency (seconds)':<30}: {round(end_time - start_time, 3)}{' s'}")


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


def count_pdf_documents(DATA_PATH):
    # Initialize a counter for PDF documents
    pdf_count = 0

    # Initialize a variable to keep track of the total size of the directory
    total_size = 0

    # Iterate through the files in the specified folder
    for filename in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, filename)

        # Check if the current path is a file and calculate its size
        if os.path.isfile(file_path):
            total_size += os.path.getsize(file_path)

            # Increment the PDF count if the file is a PDF
            if filename.endswith('.pdf'):
                pdf_count += 1
    total_size = total_size / (1024 ** 2)
    return pdf_count, total_size


def number_of_pages():
    total_pages = 0
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    doc = document_loader.load()
    for doc in doc:
        total_pages += len(doc.page_content.split('\n\n')) 
    return total_pages

if __name__ == "__main__":
    main()