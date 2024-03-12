from typing import List
from text.models.text import Text, CreateText
import uuid
from datetime import datetime
from uuid import UUID

text_lists = []

class TextController:

    def __init__(self, app, tags):
        @app.post("/v1/texts/", tags = tags)
        async def add_text(createText: CreateText) -> Text:
            text = Text(textId = uuid.uuid4(),
                               title = createText.title,
                               text = createText.text,
                               creationTimeStamp = str(datetime.now()))
            text_lists.append(text)
            return text
        
        @app.get("/v1/texts", tags = tags)
        def get_texts() -> List[Text]:
            return text_lists

        @app.get("/v1/texts/{textId}", tags = tags)
        def get_text(textId: UUID) -> Text:
            for text in text_lists:
                if text.textId == textId:
                    return text
            return {}
        
        @app.delete("/v1/texts/{textId}", tags = tags)
        async def delete_text(textId: UUID) -> Text:
            global text_lists
            selected_text = get_text(textId)
            if selected_text:
                text_lists = [text for text in text_lists if text.textId != textId]
                return selected_text
            return {}
        
        @app.put("/v1/texts/{textId}", tags = tags)
        async def put_text(textId: UUID, createText: CreateText) -> Text:
            global text_lists
            selected_text = get_text(textId)
            if selected_text:
                text_lists = [text for text in text_lists if text.textId != textId]
                text = Text(textId = selected_text.textId,
                            title = createText.title,
                            text = createText.text,
                            creationTimeStamp = str(datetime.now()))
                text_lists.append(text)
                return text
            return {}