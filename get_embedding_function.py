#from langchain_community.embeddings.ollama import OllamaEmbeddings
#from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_ollama import OllamaEmbeddings

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="llama3.1:70b")
    return embeddings
