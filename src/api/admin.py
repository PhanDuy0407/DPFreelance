from uuid import UUID
from common.database_connection import get_db
from common.helper import get_current_user
from common.constant import ADMIN_ROLE
from fastapi import APIRouter, Depends, Response, Request
from controller.AdminController import AdminController
from controller.JobController import JobController
from models.dto.input.Status import Status

router = APIRouter(prefix="/api/v1/admin", tags=["auth"])


@router.get("/jobs")
async def list(request: Request, response_model: Response, user = Depends(get_current_user([ADMIN_ROLE])), session = Depends(get_db)):
    controller = JobController(user, session)
    params = request.query_params
    result, status_code = controller.get_all_jobs(params)
    response_model.status_code = status_code
    return result

@router.get("/applies")
async def list_applies(request: Request, response_model: Response, user = Depends(get_current_user([ADMIN_ROLE])), session = Depends(get_db)):
    controller = JobController(user, session)
    params = request.query_params
    result, status_code = controller.get_all_job_applies_success(params)
    response_model.status_code = status_code
    return result

@router.put("/jobs/{job_id}/status")
async def change_status(job_id: UUID, status: Status, response_model: Response, user = Depends(get_current_user([ADMIN_ROLE])), session = Depends(get_db)):
    controller = AdminController(user, session)
    result, status_code = controller.change_job_status(str(job_id), status.status)
    response_model.status_code = status_code
    return result

@router.delete("/jobs/{job_id}")
async def delete_job(job_id: UUID, response_model: Response, user = Depends(get_current_user([ADMIN_ROLE])), session = Depends(get_db)):
    controller = AdminController(user, session)
    result, status_code = controller.delete_job(str(job_id))
    response_model.status_code = status_code
    return result

@router.get("/accounts")
async def list_account(response_model: Response, user = Depends(get_current_user([ADMIN_ROLE])), session = Depends(get_db)):
    controller = AdminController(user, session)
    result, status_code = controller.list_accounts()
    response_model.status_code = status_code
    return result

@router.put("/accounts/{account_id}/disable")
async def disable_account(account_id: UUID, response_model: Response, user = Depends(get_current_user([ADMIN_ROLE])), session = Depends(get_db)):
    controller = AdminController(user, session)
    result, status_code = controller.disable_account(str(account_id))
    response_model.status_code = status_code
    return result

@router.put("/accounts/{account_id}/enable")
async def enable_account(account_id: UUID, response_model: Response, user = Depends(get_current_user([ADMIN_ROLE])), session = Depends(get_db)):
    controller = AdminController(user, session)
    result, status_code = controller.enable_account(str(account_id))
    response_model.status_code = status_code
    return result

@router.get("/recruiters")
async def list_recruiters(response_model: Response, user = Depends(get_current_user([ADMIN_ROLE])), session = Depends(get_db)):
    controller = AdminController(user, session)
    result, status_code = controller.list_recruiters()
    response_model.status_code = status_code
    return result

@router.put("/recruiters/{recruiter_id}/post_attempt")
async def list_recruiters(recruiter_id: UUID, body: dict, response_model: Response, user = Depends(get_current_user([ADMIN_ROLE])), session = Depends(get_db)):
    controller = AdminController(user, session)
    result, status_code = controller.change_recruiter_post_attempt(str(recruiter_id), body)
    response_model.status_code = status_code
    return result

@router.get("/applicants")
async def list_applicants(response_model: Response, user = Depends(get_current_user([ADMIN_ROLE])), session = Depends(get_db)):
    controller = AdminController(user, session)
    result, status_code = controller.list_applicants()
    response_model.status_code = status_code
    return result