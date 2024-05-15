#### Talk to text 
A simple application that helps to talk with raw texts using RAG (Retrieval Augmented Generation).


#### How to get started?
Have docker pre-installed in the host / machine that you are planning to run this app, and configured as well.


1. First build the image of the app using docker

```sh
docker build -t talk-to-text:latest .
```

2. Then do docker compose, so that all the other services like vector database and nosql database comes up, that are used by the application to faciltate RAG.
```sh
docker compose up -d
```

Then go to url to access the fast API api docs to trigger the APIs (Currently only the backend is ready!)
```
https://localhost:8000
```

