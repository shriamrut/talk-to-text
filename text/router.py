from text.models.text import TextResponse, UploadText
from fastapi import Depends

from text.service import TextService

class TextRouter:

    def __init__(self, app, tags):
        self.text_service = TextService()

        @app.post("/v1/texts/", tags = tags)
        async def upload_text(uploadText: UploadText = Depends()):
            content = await uploadText.file.read()
            id = self.text_service.upload_text(content, 
                                               uploadText.title)
            return TextResponse(id = id)
        
        @app.post("/v1/texts/{id}", tags = tags)
        async def get_relevant_texts(query: str, id: str):
            return self.text_service.get_relevant_texts(text_id=id, 
                                                        query=query)
        
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