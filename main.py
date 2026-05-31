from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os

from dotenv import load_dotenv

load_dotenv()

from app.routes.perguntar import router

app = FastAPI(
    title="AutoConsult API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("URL_APP")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
async def health():

    return {
        "status": "ok"
    }