#### Talk to text 
A simple application that helps to talk with raw texts using RAG (Retrieval Augmented Generation).


#### How to get started?
Have docker pre-installed in the host / machine that you are planning to run this app, and configured as well. 

**Note: For faster performance, good to use machines having GPUs.**


1. First build the image of the app using docker

```sh
docker build -t talk-to-text:latest .
```

2. Then do docker compose, so that all the other services like vector database and nosql database comes up, that are used by the application to faciltate RAG.
```sh
docker compose up -d
```

Then go to url to access the fast API api docs to trigger the APIs, and get started.
```
http://localhost:8080/docs
```

##### Basic steps involved
1. Upload a raw text using the texts API.
2. Create a conversation using the textId obtained in the text API.
3. Then post the query that you want to get from the text to the conversation.


#### TODOs
1. Use fastAPI's router interface for multiple routings
2. Provide API way to customize the hugging face model used. Same goes for prompt template.
3. Provide API way to customize text chunking, and vectorization.
4. Add UI / UX to have a Chat UI.
5. Use multiple models in same conversations. (Query can be directed to a specific model, based on '@' annotation)
