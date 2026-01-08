from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="YouTube Health Claim Contextualizer")
app.include_router(router)
