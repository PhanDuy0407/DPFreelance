from common.database_connection import get_db
from common.helper import get_current_user
from fastapi import APIRouter, Depends, Response
from models.dto.input.Account import Account, RegisterAccount
from controller.AuthenticationController import AuthenticationController

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login")
async def login(account: Account, response_model: Response, session = Depends(get_db)):
    controller = AuthenticationController(session)
    result, status_code = controller.login(account)
    response_model.status_code = status_code
    return result

@router.post("/register")
async def register(account: RegisterAccount, response_model: Response, session = Depends(get_db)):
    controller = AuthenticationController(session)
    result, status_code = controller.register(account)
    response_model.status_code = status_code
    return result

@router.get("/me")
async def me(user =  Depends(get_current_user())):
    return user.model_dump()
