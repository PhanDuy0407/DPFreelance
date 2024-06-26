from common.database_connection import get_db
from common.helper import get_current_user
from common.constant import APPLICANT_ROLE, RECRUITER_ROLE, ADMIN_ROLE
from fastapi import APIRouter, Depends, Response, Request
from controller.JobController import JobController
from models.dto.input.Job import Job
from uuid import UUID

router = APIRouter(prefix="/api/v1/jobs", tags=["job"])

@router.get("")
async def list(request: Request, response_model: Response, session = Depends(get_db)):
    controller = JobController(None, session)
    params = request.query_params
    result, status_code = controller.get_all_jobs(params)
    response_model.status_code = status_code
    return result

@router.get("/{job_id}")
async def detail(job_id, response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = JobController(user, session)
    result, status_code = controller.get_job_by_id(job_id)
    response_model.status_code = status_code
    return result

@router.post("")
async def create_job(job: Job, response_model: Response, user = Depends(get_current_user([RECRUITER_ROLE])), session = Depends(get_db)):
    controller = JobController(user, session)
    result, status_code = controller.create_job(job)
    response_model.status_code = status_code
    return result

@router.put("/{job_id}")
async def edit(job_id: UUID, job: Job, response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = JobController(user, session)
    result, status_code = controller.edit_job(str(job_id), job)
    response_model.status_code = status_code
    return result