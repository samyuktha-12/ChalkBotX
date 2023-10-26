import parameters
from langchain.text_splitter import RecursiveCharacterTextSplitter


def text_splitter():
    return(RecursiveCharacterTextSplitter(chunk_size=parameters.chunk_size, chunk_overlap=parameters.chunk_overlap))

