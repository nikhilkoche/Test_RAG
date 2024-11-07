import pandas as pd
import psutil
from memory_profiler import memory_usage
import argparse
import time
import gc
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from get_embedding_function import get_embedding_function
from populate_database import count_pdf_documents, number_of_pages

CHROMA_PATH = "chroma"
DATA_PATH = "data"
OUTPUT_CSV = "results.csv"  # File where results will be saved

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    parser.add_argument("model_name", type=str, help="The model name to use (e.g., 'llama3.2:1b-instruct-q2_K').")
    args = parser.parse_args()
    query_text = args.query_text
    model_name = args.model_name

    # Run query_rag for the specified model
    query_rag(query_text, model_name)
    # Run the garbage collector
    gc.collect()
    

def query_rag(query_text: str, model_name: str):
    # Prepare the DB.
    mem_start = memory_usage()[0]
    start_time = time.time()
    #cpu_start = psutil.cpu_percent(interval=None)  # Start measuring CPU before the operation
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = OllamaLLM(model=model_name)
    response_text = model.invoke(prompt)
    cpu_end = psutil.cpu_percent(interval=None)  # End measuring CPU after the operation
    
    end_time = time.time()
    mem_end = memory_usage()[0]

    number_of_documents, total_size_docs = count_pdf_documents(DATA_PATH)
    num_pages = number_of_pages()
    
    # Store data in a dictionary for easy DataFrame creation
    data = {
        "Model": [model_name],
        "Total Number of Documents": [number_of_documents],
        "Total Number of Pages": [num_pages],
        "Total Size of Documents (MiB)": [round(total_size_docs, 2)],
        "Memory Usage (MiB)": [round(mem_end - mem_start, 2)],
        "Latency (seconds)": [round(end_time - start_time, 3)],
        "CPU Usage (%)": [round(cpu_end,3)],
        "Query text":[query_text],
        "Response": [response_text]
        
        
    }

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data)

    # Append the DataFrame to the CSV file
    df.to_csv(OUTPUT_CSV, mode='a', index=False, header=not pd.io.common.file_exists(OUTPUT_CSV))

    print(f"Results for model {model_name} have been saved to", OUTPUT_CSV)

if __name__ == "__main__":
    main()
