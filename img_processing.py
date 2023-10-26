import chainlit as cl
import chunks
import io
from PIL import Image
import pytesseract

async def img_processing(img_count,texts,metadatas):
    files = await cl.AskFileMessage(
            content="Please upload JPG files",
            accept=["image/jpeg"],
            max_size_mb=20,
            timeout=180,
            max_files=img_count
            ).send()
    
    i=0 #for chunk metadata
    for file in files:
        msg = cl.Message(content=f"Processing `{file.name}`...")
        await msg.send()

        # Read the PDF file
        image1=io.BytesIO(file.content)
        image = Image.open(image1)
        extracted_text = pytesseract.image_to_string(image)

        chunks.chunk_splitter(extracted_text,texts,metadatas,file,i)
        i+=1
    return texts,metadatas