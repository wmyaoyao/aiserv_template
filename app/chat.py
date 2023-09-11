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
    message: Literal['succeeded', 'failed'] = Field(
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
    # delete chat log.
    # FIXME... 
    return {"message": "reset ok"}

@app.get("/chat", response_model=ChatResults)
def chat(
    text: Annotated[
        str, 
        Query(
            title="Query string",
            description="The latest query (chat) input from user.",
            max_length=50)]) -> ChatResults:
    
    input_txt = text

    # Do something ... 
    # Generate responses ...
    # Call langchain, ...
    
    results = {"message": "succeed",
               "debug_msg": "null",
               "result": [
                   {
                   "id": 123,
                   "receive": [{"text": input_txt}],
                   "send": [
                       {"type": "text", "value": "這是bot的回答喔."},
                       {"type": "facial_expression", "value": "happy"},
                       {"type": "animation", "value": "look_around"},
                       {"type": "image", "value": "https://wmyaoyao.bot.nu:8443/anya.jpeg"},
                   ]
                   },
               ],
               }
    
    return ChatResults(**results)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)