from uuid import UUID
from common.database_connection import get_db
from common.helper import get_current_user
from common.constant import ADMIN_ROLE
from fastapi import APIRouter, Depends, Response
from models.dto.input.Recruiter import Recruiter
from controller.RecruiterController import RecruiterController

router = APIRouter(prefix="/api/v1/recruiters", tags=["recruiter"])

@router.get("")
async def list(response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = RecruiterController(user, session)
    result, status_code = controller.get_all_recruiters()
    response_model.status_code = status_code
    return result

@router.get("/{recruiter_id}")
async def detail(recruiter_id: UUID, response_model: Response, user = Depends(get_current_user(role=[ADMIN_ROLE])), session = Depends(get_db)):
    controller = RecruiterController(user, session)
    result, status_code = controller.get_recruiter_detail(str(recruiter_id))
    response_model.status_code = status_code
    return result

@router.post("/register")
async def register(recruiter_info: Recruiter, response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = RecruiterController(user, session)
    result, status_code = controller.register(recruiter_info)
    response_model.status_code = status_code
    return result