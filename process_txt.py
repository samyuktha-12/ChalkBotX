import chunks
import chainlit as cl

async def txt_processing(txt_count,texts,metadatas):
    files = await cl.AskFileMessage(
            content="Please upload text files",
            accept=["text/plain"],
            max_size_mb=20,
            timeout=180,
            max_files=txt_count
            ).send()
    
    i=0 #for chunk metadata
    for file in files:
        msg = cl.Message(content=f"Processing `{file.name}`...")
        await msg.send()

        # Decode the file
        text = file.content.decode("utf-8")

        chunks.chunk_splitter(text,texts,metadatas,file,i)
        i+=1
    return texts,metadatas