import process_scanned_pdf
import process_txt
import ppt_processing
import img_processing
import url_processing
import process_pdf
import embeddings
import models
import parameters

from chainlit.input_widget import Slider
from chainlit.input_widget import Select
from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS
import chainlit as cl
from langchain.chains import RetrievalQAWithSourcesChain
from chainlit.input_widget import TextInput
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.embeddings.openai import OpenAIEmbeddings

from dotenv import load_dotenv


messages = [
    SystemMessagePromptTemplate.from_template(parameters.system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]
prompt = ChatPromptTemplate.from_messages(messages)
chain_type_kwargs = {"prompt": prompt}


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Large Language Model",
                values=["Open-AI", "Llama 2"],
                initial_index=0,
            ),
            Select(
                id="Embeddings",
                label="Embeddings",
                values=["Open AI Embeddings", "HuggingFace Embeddings"],
                initial_index=0,
            ),
            Slider(
                id="Temperature",
                label="Temperature",
                initial=0,
                min=0,
                max=2,
                step=0.1,
            ),
            TextInput(id="chunk_size", label="Enter Chunk Size", initial="1000"),
            TextInput(id="chunk_overlap", label="Enter Chunk Overlap", initial="100"),
            TextInput(id="pdf", label="Enter number of pdf files", initial="0"),
            TextInput(id="scanned_pdf", label="Enter number of scanned pdf files", initial="0"),
            TextInput(id="txt", label="Enter number of text files", initial="0"),
            TextInput(id="ppt", label="Enter number of PPT files", initial="0"),
            TextInput(id="img", label="Enter number of Image files", initial="0"),
            TextInput(id="url", label="Enter number of URLs", initial="0"),

        ]
    ).send()


@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)
    pdf_count=int(settings["pdf"])
    txt_count=int(settings["txt"])
    scanned_pdf_count=int(settings["scanned_pdf"])
    ppt_count=int(settings["ppt"])
    img_count=int(settings["img"])
    url_count=int(settings["url"])
    model=settings["Model"]
    embed=settings["Embeddings"]
    temp=settings["Temperature"]

    parameters.chunk_overlap=int(settings["chunk_overlap"])
    parameters.chunk_size=int(settings["chunk_size"])

    elements = [
    cl.Image(name="image1", display="inline", path="./robot.jpeg")
    ]
    await cl.Message(content="Hello there, Input all relevent docs!", elements=elements).send()
    files = None

    texts=[]
    metadatas=[]
    if pdf_count!=0:
        await process_pdf.pdf_processing(pdf_count,texts,metadatas)

    if txt_count!=0:
        await process_txt.txt_processing(txt_count,texts,metadatas)
    
    if scanned_pdf_count!=0:
        await process_scanned_pdf.scanned_processing(scanned_pdf_count,texts,metadatas)
    
    if ppt_count!=0:
        await ppt_processing.ppt_processing(ppt_count,texts,metadatas)
    
    if img_count!=0:
        await img_processing.img_processing(img_count,texts,metadatas)

    if url_count!=0:
        await url_processing.url_processing(url_count,texts,metadatas)


    # Create Embeddings
    emb=embeddings.select_embeddings(embed)
    if embed=='Open AI Embeddings':
        docsearch = await cl.make_async(Chroma.from_texts)(texts, emb, metadatas=metadatas, persist=parameters.CHROMA_PATH)
    else:
        docsearch = await cl.make_async(FAISS.from_texts)(texts, emb, metadatas=metadatas)
        docsearch.save_local(parameters.DB_FAISS_PATH)
    

    # Choose LLM
    llm=models.select_model(model,temp)
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type=parameters.type,
        retriever=docsearch.as_retriever(),
    )

    # Save the metadata and texts in the user session
    cl.user_session.set("metadatas", metadatas)
    cl.user_session.set("texts", texts)

    print(texts)
    print(metadatas)

    # Let the user know that the system is ready
    msg= cl.Message(content=f"Processing done. You can now ask questions!")
    await msg.send()

    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message:str):
 
    message=""
    chain = cl.user_session.get("chain")  
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    res = await chain.acall(message, callbacks=[cb])
    print(res)
    answer = res["answer"]
    sources=False
    source_elements = []

    # Get the metadata and texts from the user session
    metadatas = cl.user_session.get("metadatas")
    all_sources = [m["source"] for m in metadatas]
    texts = cl.user_session.get("texts")

    if sources:
        found_sources = []

        # Add the sources to the message
        for source in sources.split(","):
            source_name = source.strip()

            # Get the index of the source
            try:
                index = all_sources.index(source_name)

            except ValueError:
                print("value error in finding source")
                continue
            text = texts[index]
            found_sources.append(source_name)
            
            # Create the text element referenced in the message
            source_elements.append(cl.Text(content=text, name=source_name))

        if found_sources:
            answer += f"\nSources: {', '.join(found_sources)}"
        else:
            answer += "\nNo sources found"

    if cb.has_streamed_final_answer:
        cb.final_stream.elements = source_elements
        await cb.final_stream.update()
    else:
        await cl.Message(content=answer, elements=source_elements).send()
    