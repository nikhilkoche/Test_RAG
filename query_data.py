import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
#from langchain_community.llms.ollama import Ollama
from langchain_ollama import OllamaLLM
import time
from get_embedding_function import get_embedding_function
from populate_database import count_pdf_documents,number_of_pages
CHROMA_PATH = "chroma"

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
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)
    start_time = time.time()
    model = OllamaLLM(model="llama3.1:70b")
    response_text = model.invoke(prompt)
    end_time=time.time()
    #sources = [doc.metadata.get("id", None) for doc, _score in results]
    #formatted_response = f"Response: {response_text}\nSources: {sources}"
    formatted_response = f"Response: {response_text}"
    number_of_documents = count_pdf_documents()
    num_pages = number_of_pages()
    # print(formatted_response)
    # print(f'Total number of Documents: {number_of_documents} and total number of pages:{num_pages}')
    # print("Inference Time(in seconds):",round(end_time-start_time,3))
    # print(f'Model:',{model.model})
    print(formatted_response)
    print(f"{'Total Number of Documents':<30}: {number_of_documents}")
    print(f"{'Total Number of Pages':<30}: {num_pages}")
    print(f"{'Latency (seconds)':<30}: {round(end_time - start_time, 3)}")
    print(f"{'Model':<30}: {model.model}")



if __name__ == "__main__":
    main()
