from fastapi import APIRouter, Depends
from SRC.models.usuaris import *
from SRC.services.usuaris import *

async def get_usuaris_service():
    return UsuariService()

router = APIRouter(
    prefix="/usuaris",
    tags=["usuaris"],
    responses={404: {"description": "Not found"}}
)
@router.get("/", response_model=List[Usuari])
async def all_users(
        usuari_service: UsuariService = Depends(UsuariService)
    ):
    return usuari_service.get_all_Usuaris()

@router.get("/{id}", response_model=Usuari)
async def user_by_id(
        id: int,
        usuari_service: UsuariService = Depends(UsuariService)
    ):
    return usuari_service.get_Usuari_by_id(id)

@router.post("/", response_model=Usuari)
async def create_new_user(
        Create: CreateUsuari,
        usuari_service: UsuariService = Depends(UsuariService)
    ):
    return usuari_service.create_Usuari(Create.name, Create.mail, Create.hash)

@router.post("/authenticate/", response_model=Usuari)
async def authenticate(
        Auth: AuthRequest,
        usuari_service: UsuariService = Depends(UsuariService)
    ):
    return usuari_service.authenticate_Usuari(Auth.name, Auth.hash)

@router.put("/{id}/name", response_model=Usuari)
async def update_user_name(
        id: int,
        update_data: UpdateUsuariName,
        usuari_service: UsuariService = Depends(UsuariService)
    ):
    return usuari_service.update_Usuari_name(id, update_data.name)

@router.put("/{id}/mail", response_model=Usuari)
async def update_user_mail(
        id: int,
        update_data: UpdateUsuariMail,
        usuari_service: UsuariService = Depends(UsuariService)
    ):
    return usuari_service.update_Usuari_mail(id, update_data.mail)

@router.put("/{id}/password", response_model=Usuari)
async def update_user_password(
        id: int,
        update_data: UpdateUsuariPassword,
        usuari_service: UsuariService = Depends(UsuariService)
    ):
    return usuari_service.update_Usuari_password(id, update_data.hash)


@router.delete("{id}", response_model=dict)
async def delete_user(
        id: int,
        usuari_service: UsuariService = Depends(UsuariService)
    ):
    return usuari_service.delete_Usuari_by_id(id)