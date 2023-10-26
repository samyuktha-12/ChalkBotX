#Text Splitter Parameters
chunk_size=1000
chunk_overlap=100

#Scanned PDF Parameters
folder_dir="images_path"
output_dir="pages"
inpath="inpath"
pdfpath="result"
pdf_folder="pages"
directory_path=["inpath","images_path","pages"]

#ChainRetrieval parameters
type="stuff"

#Datastores Path
DB_FAISS_PATH="FAISS"
CHROMA_PATH="chroma_db"

#Template
system_template = """Use the following pieces of context to answer the users question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
ALWAYS return a "SOURCES" part in your answer.
The "SOURCES" part should be a reference to the source of the document from which you got your answer.

Example of your response should be:

```
The answer is foo
SOURCES: xyz
```

Begin!
----------------
{summaries}"""