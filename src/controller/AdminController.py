from http import HTTPStatus
from uuid import uuid4
from datetime import datetime

from persistent.AccountPersistent import AccountPersistent
from persistent.JobPersistent import JobPersistent
from models.dto.output.JobDTO import RecruiterJobDTO as AdminJobDTO
from models.dto.output.JobDTO import JobDTO
from models.dto.output.RecruiterJobPricing import RecruiterJobPricing
from models.dto.output.ApplicantDTO import ApplicantDTO
from models.dto.output.RecruiterDTO import RecruiterDTO, RecruiterInfoDTO
from models.dto.output.UserInformation import UserInformation
from models.dto.output.AccountDTO import Account
from models.dto.output.CategoryDTO import CategoryDTO
from controller.model.ResponseModel import ListResponseModel, ResponseModel
from common.constant import JobStatus
from controller.NotificationController import NotificationController

class AdminController:
    def __init__(self, user: Account, session) -> None:
        self.user = user
        self.session = session
        self.account_persistent = AccountPersistent(session)
        self.job_persistent = JobPersistent(session)
        self.notification = NotificationController(user, session)

    def list_jobs(self, params):
        job_detail = self.job_persistent.get_all_jobs(params)
        result = []
        for job, category, poster, poster_account in job_detail:
            job_applied=self.job_persistent.get_job_applied_success_by_job_id(job.id)
            if job_applied:
                job_apply, applicant, account = job_applied
                job_applied = RecruiterJobPricing(
                    applicant=ApplicantDTO(
                        **applicant.to_dict(),
                        information=UserInformation(**account.to_dict())
                    ),
                    **job_apply.to_dict()
                )
            result.append(
                AdminJobDTO(
                    **job.to_dict(), 
                    category=CategoryDTO(**category.to_dict()),
                    poster=RecruiterDTO(
                        **poster.to_dict(),
                        information=UserInformation(
                            **poster_account.to_dict(),
                        )
                    ),
                    job_applied=job_applied,
                    number_of_pricing=len(self.job_persistent.get_jobs_apply_by_job_id(job.id))
                )
            )
        return ListResponseModel(
            data=result,
            detail="Success",
            total=len(result)
        ).model_dump(), HTTPStatus.OK
    
    def change_job_status(self, job_id, status):
        job_detail = self.job_persistent.get_job_by_id(job_id)
        if not job_detail:
            return ResponseModel(
                detail="Job not found"
            ), HTTPStatus.NOT_FOUND

        job, category, poster, poster_account = job_detail
        if status == JobStatus.DENY and job.status != JobStatus.WAITING_FOR_APPROVE:
            return ResponseModel(
                detail=f"Cannot deny job with status {job.status}"
            ), HTTPStatus.BAD_REQUEST
        if status == JobStatus.OPEN and job.status != JobStatus.WAITING_FOR_APPROVE:
            return ResponseModel(
                detail=f"Cannot apply job with status {job.status}"
            ), HTTPStatus.BAD_REQUEST
        if status == JobStatus.CLOSED and job.status not in [JobStatus.OPEN, JobStatus.REOPEN]:
            return ResponseModel(
                detail=f"Cannot close job with status {job.status}"
            ), HTTPStatus.BAD_REQUEST
        if status == JobStatus.DONE and job.status != JobStatus.WORK_IN_PROGRESS:
            return ResponseModel(
                detail=f"Cannot close job with status {job.status}"
            ), HTTPStatus.BAD_REQUEST
        
        if status not in [JobStatus.OPEN, JobStatus.REOPEN, JobStatus.CLOSED, JobStatus.DENY, JobStatus.DONE]:
            return ResponseModel(
                detail=f"Cannot update job status to {status}, valid status is {[JobStatus.OPEN, JobStatus.REOPEN, JobStatus.CLOSED, JobStatus.DENY, JobStatus.DONE]}"
            ), HTTPStatus.BAD_REQUEST
        
        job.status = status
        self.session.commit()
        if status == JobStatus.OPEN:
            self.notification.send_notification_to_recruiter(
                recruiter_id=poster.id,
                content=f"Tin tuyển dụng của bạn đã được duyệt",
                nav_link=f"recruiters/jobs/{job_id}",
                avatar="https://media.istockphoto.com/id/1456608170/photo/3d-chat-bot-robot-conversation-voice-support.webp?b=1&s=170667a&w=0&k=20&c=LrXzTb7byEQP3nkvklF75Y9PF7Fjnola-A_TztLFZ0M="
            )
        if status == JobStatus.DENY:
            self.notification.send_notification_to_recruiter(
                recruiter_id=poster.id,
                content=f"Tin tuyển dụng của bạn đã bị từ chối",
                nav_link=f"recruiters/jobs/{job_id}",
                avatar="https://media.istockphoto.com/id/1456608170/photo/3d-chat-bot-robot-conversation-voice-support.webp?b=1&s=170667a&w=0&k=20&c=LrXzTb7byEQP3nkvklF75Y9PF7Fjnola-A_TztLFZ0M=",
            )
        return ResponseModel(
            data=JobDTO(
                **job.to_dict(), 
                category=CategoryDTO(**category.to_dict()),
                poster=RecruiterDTO(
                    **poster.to_dict(),
                    information=UserInformation(
                        **poster_account.to_dict(),
                    )
                )
            ),
            detail="Success",
        ).model_dump(), HTTPStatus.NO_CONTENT

    def delete_job(self, job_id):
        job_detail = self.job_persistent.get_job_by_id(job_id)
        if not job_detail:
            return ResponseModel(
                detail="Job not found"
            ), HTTPStatus.NOT_FOUND

        job, _, _, _ = job_detail
        if job.status != JobStatus.CLOSED:
            return ResponseModel(
                detail=f"Cannot close job with status {job.status}"
            ), HTTPStatus.BAD_REQUEST
        self.job_persistent.delete_job(job)
        return ResponseModel(
            detail="Success",
        ).model_dump(), HTTPStatus.NO_CONTENT
    
    def list_accounts(self):
        accounts_detail = self.account_persistent.get_all_account()
        result = []
        for account, applicant, recruiter in accounts_detail:
            user_dict = account.to_dict()
            result.append(
                Account(
                    **user_dict,
                    applicant=ApplicantDTO(**applicant.to_dict(), information=UserInformation(**user_dict)) if applicant else None,
                    recruiter=RecruiterInfoDTO(**recruiter.to_dict(), information=UserInformation(**user_dict)) if recruiter else None
                )
            )
        return ListResponseModel(
            data=result,
            detail="Success",
            total=len(result)
        ).model_dump(), HTTPStatus.OK
    
    def disable_account(self, account_id):
        self.account_persistent.toggle_account(account_id, 0)
        return ResponseModel(
            detail="Success"
        ), HTTPStatus.OK
    
    def enable_account(self, account_id):
        self.account_persistent.toggle_account(account_id, 1)
        return ResponseModel(
            detail="Success"
        ), HTTPStatus.OK