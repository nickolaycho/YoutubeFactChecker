from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="YouTube Fact Checker")
app.include_router(router)
