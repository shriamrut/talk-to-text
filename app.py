from text.controller import TextController
from chat.conversation.controller import ConversationController
from fastapi import FastAPI
import logging

app = FastAPI(title = "Talk to Text", summary = "An app that can help you talk to your texts using through chat")
conversation_controller = ConversationController(app, tags=["Conversation Controller"])
text_controller = TextController(app, tags=["Text Controller"])
if __name__ == "__main__":
    app.run()