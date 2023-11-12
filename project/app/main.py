from fastapi import FastAPI
from .routers import companies, documents, users

app = FastAPI(docs_url="/docs")
app.include_router(companies.router)
app.include_router(documents.router)
app.include_router(users.router)

@app.get("/health")
async def pong():
    return {"message": "healthy"}

@app.get("/")
async def root():
    return {"message": "Hello World"}

