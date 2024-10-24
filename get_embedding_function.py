#from langchain_community.embeddings.ollama import OllamaEmbeddings
#from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    # embeddings = HuggingFaceEmbeddings(
    #     model_name="thenlper/gte-base"
    
    
    return embeddings

def get_embedding_function_hug():
    embeddings = HuggingFaceEmbeddings('thenlper/gte-base')
    return embeddings
