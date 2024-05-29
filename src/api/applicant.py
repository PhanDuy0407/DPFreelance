from uuid import UUID
from common.database_connection import get_db
from common.helper import get_current_user
from common.constant import ADMIN_ROLE
from fastapi import APIRouter, Depends, Response
from models.dto.input.Applicant import Applicant
from controller.ApplicantController import ApplicantController

router = APIRouter(prefix="/api/v1/applicants", tags=["applicant"])

@router.get("")
async def list(response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = ApplicantController(user, session)
    result, status_code = controller.get_all_applicants()
    response_model.status_code = status_code
    return result

@router.get("/my-jobs")
async def get_job_applied(response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = ApplicantController(user, session)
    result, status_code = controller.get_job_applied()
    response_model.status_code = status_code
    return result

@router.get("/{applicant_id}")
async def detail(applicant_id: UUID, response_model: Response, user = Depends(get_current_user(role=[ADMIN_ROLE])), session = Depends(get_db)):
    controller = ApplicantController(user, session)
    result, status_code = controller.get_applicant_by_id(str(applicant_id))
    response_model.status_code = status_code
    return result

@router.post("/register")
async def register(applicant_info: Applicant, response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = ApplicantController(user, session)
    result, status_code = controller.register(applicant_info)
    response_model.status_code = status_code
    return result