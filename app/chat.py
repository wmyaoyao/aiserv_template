# Python version >= 3.10

import asyncio
import os
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Annotated, Literal

description = """
A chatbot API for demo.

List of APIs:
  - chat: Main query api
  - reset: Reset chat session.
"""

app = FastAPI(
    title = "Chatbot API",
    description = description,
    summary = "This is a summary",
    version = "0.1",
)

app.state.chatid = 1
app.state.user_chat_log = []
app.state.bot_history = []

class ReceiveMsg(BaseModel):
    text: str

class SendMsg(BaseModel):
    type: Literal['text', 'facial_expression', 'animation', 'image']
    value: str

class ChatSession(BaseModel):
    id: int = Field(
        description = "Unique identifier for the chat session.")
    receive: list[ReceiveMsg] = Field(
        description = "An array of messages received by the bot(chat engine).")
    send: list[SendMsg] = Field(
        description = "An array of messages sent from the bot to the user.")

class ChatResults(BaseModel):
    message: Literal['succeed', 'failed'] = Field(
        description = "Status of the request.")
    degug_msg: str = Field(
        default = "null", 
        description = "Debug message.")
    result: list[ChatSession] = Field(
        description = "Interaction details between user input and bot responses.")

# Demo functions
@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/reset")
def reset_chat():
    app.state.user_chat_log = []
    app.state.bot_history = []
    app.state.chatid += 1
    return {"state": app.state}

@app.get("/chat_v1", response_model=ChatResults)
def chat(text: Annotated[
        str, Query(
                title="Query string",
                description="The latest query (chat) input from user.",
                max_length=50)]) -> ChatResults:
    
    input_txt = text
    output_txt = bot_reply(input_txt)
    app.state.user_chat_log.insert(0, {"text": input_txt})
    
    results = {"message": "succeed",
               "debug_msg": "null",
               "result": [
                   {
                   "id": app.state.chatid,
                   "receive": app.state.user_chat_log,
                   "send": gen_sendobj(output_txt),
                   },
               ],
               }
    
    return ChatResults(**results)

@app.get("/chat_v2", response_model=ChatResults)
def chat(text: Annotated[
        str, Query(
                title="Query string",
                description="The latest query (chat) input from user.",
                max_length=50)]) -> ChatResults:
    
    input_txt = text
    output_txt = bot_reply(input_txt)
    app.state.user_chat_log.insert(0, {"text": input_txt})
    app.state.bot_history.insert(0, {
                   "id": app.state.chatid,
                   "receive": app.state.user_chat_log.copy(),
                   "send": gen_sendobj(output_txt),
                   })

    results = {"message": "succeed",
               "debug_msg": "null",
               "result": app.state.bot_history.copy(),
               }
    
    return ChatResults(**results)


# Some helper functions.

def gen_sendobj(output_txt):
    sendobj = []
    sendobj.append({"type": "text", "value": output_txt})
    sendobj.append({"type": "facial_expression", "value": "happy"})
    sendobj.append({"type": "animation", "value": "look_around"})
    sendobj.append({"type": "image", "value": "https://wmyaoyao.bot.nu:8443/anya.jpeg"})
    return sendobj

def bot_reply(input_txt):
    cnt = len(app.state.user_chat_log)
    output_txt = "reply{:02d}: {}".format(cnt ,input_txt)
    return output_txt



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)