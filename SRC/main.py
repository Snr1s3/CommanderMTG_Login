from fastapi import FastAPI, HTTPException, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import date

from .models import *

from .client import *

from .routers.users import *

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

@app.get("/all_users", response_model=List[User])
def all_users():
    return get_all_Users()

@app.get("/user/{id}", response_model=User)
def user_by_id(id: int):
    return get_User_by_id(id)

@app.post("/user/create", response_model=User)
def create_new_user(Auth: AuthRequest):
    return create_User(Auth.name, Auth.pwd)

@app.post("/user/authenticate/", response_model=User)
def authenticate(Auth: AuthRequest):
    return authenticate_User(Auth.name, Auth.pwd)

@app.put("/user/update", response_model=User)
def update_user(Update: UpdateRequest):
    return update_User(Update.id, Update.name, Update.mail, Update.pwd)

@app.delete("/user/delete", response_model=dict)
def delete_user(id: int):
    return delete_User_by_id(id)