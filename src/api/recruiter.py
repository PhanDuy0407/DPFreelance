from uuid import UUID
from common.database_connection import get_db
from common.helper import get_current_user
from common.constant import ADMIN_ROLE, RECRUITER_ROLE
from fastapi import APIRouter, Depends, Response, Request
from models.dto.input.Recruiter import Recruiter
from models.dto.input.ApplyStatus import ApplyStatus
from controller.RecruiterController import RecruiterController
from controller.JobController import JobController

router = APIRouter(prefix="/api/v1/recruiters", tags=["recruiter"])

@router.get("")
async def list(response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = RecruiterController(user, session)
    result, status_code = controller.get_all_recruiters()
    response_model.status_code = status_code
    return result

@router.post("/register")
async def register(recruiter_info: Recruiter, response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = RecruiterController(user, session)
    result, status_code = controller.register(recruiter_info)
    response_model.status_code = status_code
    return result

@router.get("/jobs")
async def get_all_jobs_posted(request: Request, response_model: Response, user = Depends(get_current_user([RECRUITER_ROLE])), session = Depends(get_db)):
    controller = JobController(user, session)
    params = request.query_params
    result, status_code = controller.get_all_recruiter_jobs_posted(params)
    response_model.status_code = status_code
    return result

@router.get("/jobs/{job_id}/applies")
async def get_all_job_applies(job_id: UUID, response_model: Response, user = Depends(get_current_user([RECRUITER_ROLE])), session = Depends(get_db)):
    controller = JobController(user, session)
    result, status_code = controller.get_all_recruiter_jobs_apply(str(job_id))
    response_model.status_code = status_code
    return result

@router.put("/jobs/{job_id}/applies/{applicant_id}")
async def change_job_apply_status(job_id: UUID, applicant_id: UUID, job_apply_status: ApplyStatus, response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = JobController(user, session)
    result, status_code = controller.change_job_apply_status(str(job_id), str(applicant_id), job_apply_status)
    response_model.status_code = status_code
    return result

@router.put("/jobs/{job_id}/mark_done")
async def mark_done(job_id: UUID, response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = JobController(user, session)
    result, status_code = controller.recruiter_mark_done_job(str(job_id))
    response_model.status_code = status_code
    return result

@router.get("/{recruiter_id}")
async def detail(recruiter_id: UUID, response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = RecruiterController(user, session)
    result, status_code = controller.get_recruiter_detail(str(recruiter_id))
    response_model.status_code = status_code
    return result

@router.get("/{recruiter_id}/statistics")
async def statistics(recruiter_id: UUID, response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = RecruiterController(user, session)
    result, status_code = controller.get_recruiter_statistic_by_id(str(recruiter_id))
    response_model.status_code = status_code
    return result