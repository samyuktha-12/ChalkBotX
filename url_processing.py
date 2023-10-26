import chainlit as cl
import requests
import chunks

async def url_processing(url_count,texts,metadatas):
    urls = await cl.AskUserMessage(
            content="Please upload urls (as comma separated text)",
            ).send()
    urls=urls['content'].split(",")
    for url in urls:
        i=0 #for chunk metadata
        msg = cl.Message(content=f"Processing ...")
        await msg.send()
        
        response = requests.get(url)
        if response.status_code != 200:
            return None, f"Failed to fetch content from the URL: {url}"
        content = response.text
        url_text= content.split("\n\n")  # Split by double line breaks (paragraphs)

        chunks.chunk_splitter(url_text,texts,metadatas,url,i)
        i+=1
    return texts,metadatas