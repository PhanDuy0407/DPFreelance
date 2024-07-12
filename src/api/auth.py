from common.database_connection import get_db
from common.helper import get_current_user
from fastapi import APIRouter, Depends, Response, UploadFile, File
from models.dto.input.Account import Account, RegisterAccount, ResetPassword
from controller.AuthenticationController import AuthenticationController

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login")
async def login(account: Account, response_model: Response, session = Depends(get_db)):
    controller = AuthenticationController(session)
    result, status_code = controller.login(account)
    response_model.status_code = status_code
    return result

@router.put("/reset_password")
async def login(reset_password: ResetPassword, response_model: Response, user =  Depends(get_current_user()), session = Depends(get_db)):
    controller = AuthenticationController(session)
    result, status_code = controller.reset_password(user, reset_password)
    response_model.status_code = status_code
    return result

@router.post("/admin/login")
async def login(account: Account, response_model: Response, session = Depends(get_db)):
    controller = AuthenticationController(session)
    result, status_code = controller.login_admin(account)
    response_model.status_code = status_code
    return result

@router.post("/register")
async def register(account: RegisterAccount, response_model: Response, session = Depends(get_db)):
    controller = AuthenticationController(session)
    result, status_code = controller.register(account)
    response_model.status_code = status_code
    return result

@router.post("/upload-avatar")
async def upload_avartar(avatar: UploadFile = File(...), response_model: Response = None,  session = Depends(get_db)):
    controller = AuthenticationController(session)
    result, status_code = controller.upload_avatar(avatar)
    response_model.status_code = status_code
    return result

@router.get("/me")
async def me(user =  Depends(get_current_user())):
    return user.model_dump()
