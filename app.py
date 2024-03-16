from text.router import TextRouter
from chat.conversation.router import ConversationRouter
from fastapi import FastAPI

app = FastAPI(title = "Talk to Text", summary = "An app that can help you talk to your texts using through chat")
ConversationRouter(app, tags=["Conversation Controller"])
TextRouter(app, tags=["Text Controller"])

if __name__ == "__main__":
    app.run()