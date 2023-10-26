from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings

def select_embeddings(embed):
    if embed=='Open AI Embeddings':
         embeddings = OpenAIEmbeddings()
         return embeddings
    else:
        model_id = 'sentence-transformers/all-MiniLM-L6-v2'
        model_kwargs = {'device': 'cpu'}
        hf_embedding = HuggingFaceEmbeddings(model_name=model_id, model_kwargs=model_kwargs)
        return hf_embedding
