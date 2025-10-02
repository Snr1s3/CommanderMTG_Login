from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .client import *
from .services.usuaris import *
from SRC.routers import usuaris
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


app.include_router(usuaris.router)
@app.get("/", response_model=str)
def root():
    return "API de Turnonauta operativa"

