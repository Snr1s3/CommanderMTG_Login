from fastapi import FastAPI, HTTPException, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import date

from .models import *

from .client import *

from .routers.user import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/", response_model=str)
def root():
    return "API de Turnonauta operativa"

@app.get("/all_players", response_model=List[player])
def all_players():
    return get_all_players()

@app.get("/player/{id}", response_model=player)
def player_by_id(id: int):
    return get_player_by_id(id)

@app.post("/player/create", response_model=player)
def create_new_player(Auth: AuthRequest):
    return create_player(Auth.name, Auth.pwd)

@app.post("/player/authenticate/", response_model=player)
def authenticate(Auth: AuthRequest):
    return authenticate_player(Auth.name, Auth.pwd)

@app.put("/player/update", response_model=player)
def update_player(Auth: AuthRequest):
    return update_player_hash(Auth.name, Auth.pwd)

@app.delete("/player/delete", response_model=dict)
def delete_player(id: int):
    return delete_player_by_id(id)