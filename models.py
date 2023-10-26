from langchain.chat_models import ChatOpenAI
from langchain.llms import CTransformers
import langchain

def select_model(model,temp):
    if model=='Open-AI':
        llm = ChatOpenAI(temperature=temp)
        return llm
    else:
        llm = CTransformers(
        model="model\llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type='llama',
        config={'max_new_tokens': 256, 'temperature': temp})
        return llm



    