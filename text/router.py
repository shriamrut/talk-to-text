from text.models.text import TextResponse, UploadText
from fastapi import Depends

from text.service import TextService

class TextRouter:

    def __init__(self, app, tags):
        self.text_service = TextService()

        @app.post("/v1/texts/", tags = tags)
        async def upload_text(uploadText: UploadText = Depends()):
            content = await uploadText.file.read()
            id = self.text_service.upload_text(content_in_bytes=content, 
                                               title=uploadText.title,
                                               chunk_size=uploadText.chunkSize,
                                               chunk_overlap=uploadText.chunkOverlap)
            return TextResponse(id = id)
        
        @app.post("/v1/texts/{id}", tags = tags)
        async def get_relevant_texts(query: str, id: str, referenceChunkCount: int):
            return self.text_service.get_relevant_texts(text_id=id, 
                                                        query=query,
                                                        reference_chunk_count=referenceChunkCount)