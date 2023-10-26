import chunks
import PyPDF2
import chainlit as cl
from io import BytesIO

async def pdf_processing(pdf_count,texts,metadatas):
    files = await cl.AskFileMessage(
            content="Please upload PDF files",
            accept=["application/pdf"],
            max_size_mb=20,
            timeout=180,
            max_files=pdf_count
            ).send()
    
    i=0
    for file in files:
        msg = cl.Message(content=f"Processing `{file.name}`...")
        await msg.send()

        pdf_stream = BytesIO(file.content)
        pdf = PyPDF2.PdfReader(pdf_stream)
        pdf_text = ""
        for page in pdf.pages:
            pdf_text += page.extract_text()
        chunks.chunk_splitter(pdf_text,texts,metadatas,file,i)
        i+=1

    return texts,metadatas
