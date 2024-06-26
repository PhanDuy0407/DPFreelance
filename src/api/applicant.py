from uuid import UUID
from common.database_connection import get_db
from common.helper import get_current_user
from common.constant import APPLICANT_ROLE
from fastapi import APIRouter, Depends, Response, Request
from models.dto.input.Applicant import Applicant
from controller.ApplicantController import ApplicantController
from controller.JobController import JobController

router = APIRouter(prefix="/api/v1/applicants", tags=["applicant"])

@router.get("")
async def list(response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = ApplicantController(user, session)
    result, status_code = controller.get_all_applicants()
    response_model.status_code = status_code
    return result

@router.get("/jobs")
async def get_job_applied(request: Request, response_model: Response, user = Depends(get_current_user([APPLICANT_ROLE])), session = Depends(get_db)):
    controller = JobController(user, session)
    params = request.query_params
    result, status_code = controller.get_job_applicant_applied(params)
    response_model.status_code = status_code
    return result

@router.post("/jobs/{job_id}/apply")
async def apply_job(job_id: UUID, response_model: Response, user = Depends(get_current_user([APPLICANT_ROLE])), session = Depends(get_db)):
    controller = JobController(user, session)
    result, status_code = controller.apply_job(str(job_id))
    response_model.status_code = status_code
    return result

@router.put("/jobs/{job_id}/revoke")
async def revoke_apply_job(job_id: UUID, response_model: Response, user = Depends(get_current_user([APPLICANT_ROLE])), session = Depends(get_db)):
    controller = JobController(user, session)
    result, status_code = controller.revoke_job_apply(str(job_id))
    response_model.status_code = status_code
    return result

@router.get("/{applicant_id}")
async def detail(applicant_id: UUID, response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = ApplicantController(user, session)
    result, status_code = controller.get_applicant_by_id(str(applicant_id))
    response_model.status_code = status_code
    return result

@router.get("/{applicant_id}/statistics")
async def statistics(applicant_id: UUID, response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = ApplicantController(user, session)
    result, status_code = controller.get_applicant_statistic_by_id(str(applicant_id))
    response_model.status_code = status_code
    return result

@router.post("/register")
async def register(applicant_info: Applicant, response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = ApplicantController(user, session)
    result, status_code = controller.register(applicant_info)
    response_model.status_code = status_code
    return result