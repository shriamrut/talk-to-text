from inventory.embedding_collection import EmbeddingCollection
from inventory.text_collection import TextCollection
from text.models.text import TextResponse, UploadText
from fastapi import Depends

class TextRouter:

    def __init__(self, app, tags):
        self.embedding_collection = EmbeddingCollection()
        self.text_collection = TextCollection()

        @app.post("/v1/texts/", tags = tags)
        async def upload_text(uploadText: UploadText = Depends()):
            content = await uploadText.file.read()
            file_content = content.decode("utf-8")
            id = self.text_collection.create(file_content, uploadText.title)
            self.embedding_collection.create(file_content, text_id=id)
            return TextResponse(id = id)
        
        @app.post("/v1/texts/{id}", tags = tags)
        async def get_relevant_texts(query: str, id: str):
            return self.embedding_collection.query(text_id = id, 
                                                   query_text = query)
        
        '''
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
    '''