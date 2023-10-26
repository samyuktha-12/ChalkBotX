import parameters
import textsplitter

# Split the text into chunks
splitter=textsplitter.text_splitter()

def chunk_splitter(text,texts,metadatas,file,i):
    chunks=splitter.split_text(text)
    for chunk in chunks:
        texts.append(chunk)
        metadatas.append({"source": f"{file.name}:chunk {i}"})
    return texts,metadatas