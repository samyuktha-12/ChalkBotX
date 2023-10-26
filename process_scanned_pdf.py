import chainlit as cl
import parameters
import scanned_to_searchable
import PyPDF2
import chunks
from io import BytesIO
import os

async def scanned_processing(scanned_pdf_count,texts,metadatas):
    files = await cl.AskFileMessage(
            content="Please upload Scanned PDF files",
            accept=["application/pdf"],
            max_size_mb=20,
            timeout=180,
            max_files=scanned_pdf_count
            ).send()
    
    i=0 #for chunk metadata
    for file in files:
        msg = cl.Message(content=f"Processing `{file.name}`...")
        await msg.send()

        # Read the PDF file
        pdf_stream = BytesIO(file.content)
        pdf = PyPDF2.PdfReader(pdf_stream)
        output_pdf=PyPDF2.PdfWriter()
        for page in pdf.pages:
            output_pdf.add_page(page)
        completeName = os.path.join(parameters.inpath, file.name)
        output_pdf.write(completeName)
        scanned_to_searchable.image_conversion(completeName)
        scanned_to_searchable.pdf_conversion(parameters.folder_dir)
        scanned_to_searchable.merge_pdf(parameters.pdf_folder,file.name)
        for p in parameters.directory_path:
            scanned_to_searchable.delete_files_in_directory(p)

        # Read the Searchable PDF file
        pdf = PyPDF2.PdfReader(parameters.pdfpath+'/'+file.name+".pdf")
        pdf_text = ""
        for page in pdf.pages:
            pdf_text += page.extract_text()

        # Split the text into chunks
        chunks.chunk_splitter(pdf_text,texts,metadatas,file,i)
        i+=1
    scanned_to_searchable.delete_files_in_directory(parameters.pdfpath)
    return texts,metadatas

