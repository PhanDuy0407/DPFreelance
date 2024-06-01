import uuid
from http import HTTPStatus
from datetime import datetime, timedelta

from persistent.JobPersistent import JobPersistent
from persistent.RecruiterPersistent import RecruiterPersistent
from models.dto.output.JobDTO import JobDTO as OutputJob
from models.dto.output.JobApplyDTO import JobApplyDTO, RecruiterJobPricing, ApplicantJobPricing
from models.dto.input.Job import Job as InputJob
from models.dto.input.JobApply import JobApply, JobApplyStatus
from models.dto.output.RecruiterDTO import RecruiterDTO
from models.dto.output.ApplicantDTO import ApplicantDTO
from models.dto.output.UserInformation import UserInformation
from models.dto.output.CategoryDTO import CategoryDTO
from models.dto.output.AccountDTO import Account
from models.data.Job import Job
from models.data.JobApply import JobApply as JobApplyData
from controller.model.ResponseModel import ListResponseModel, ResponseModel
from common.constant import JobPricingStatus, JobStatus

class JobController:
    def __init__(self, user: Account, session) -> None:
        self.user = user
        self.persistent = JobPersistent(session)
        self.recruiter_persistent = RecruiterPersistent(session)

    def get_all_jobs(self, params = {}):
        job_detail = self.persistent.get_all_jobs(params)
        result = [
            OutputJob(
                **job.to_dict(), 
                category=CategoryDTO(**category.to_dict()),
                poster=RecruiterDTO(
                    **poster.to_dict(),
                    information=UserInformation(
                        **poster_account.to_dict(),
                    )
                )
            ) 
            for job, category, poster, poster_account  in job_detail
        ]
        return ListResponseModel(
            data=result,
            detail="Success",
            total=len(result)
        ).model_dump(), HTTPStatus.OK
    
    def get_job_by_id(self, job_id):
        job_detail = self.persistent.get_job_by_id(job_id)
        if not job_detail:
            return ResponseModel(
                detail="Job not found"
            ), HTTPStatus.NOT_FOUND

        job, category, poster, poster_account = job_detail
        return ResponseModel(
            data=OutputJob(
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
        ).model_dump(), HTTPStatus.OK
    
    def create_job(self, job: InputJob):
        if self.user.recruiter.free_post_attempt <= 0 and self.user.recruiter.remain_post_attempt <= 0:
            return ResponseModel( 
                detail="No more post job attemps",
            ).model_dump(), HTTPStatus.CONFLICT

        job_record = Job(
            id=str(uuid.uuid4()),
            name=job.name,
            category_id=job.category_id,
            poster_id=self.user.recruiter.id,
            description=job.description,
            jd_file=job.jd_file,
            price=job.price,
            price_unit=job.price_unit,
            type=job.type,
            status="OPEN",
            estimate_time=job.estimate_time,
            end_date=job.end_date,
            created_at=datetime.now(),
        )
        self.persistent.add_job(job_record)
        if self.user.recruiter.free_post_attempt > 0:
            self.recruiter_persistent.reset_free_post_attempt(recruiter_id=self.user.recruiter.id)
        elif self.user.recruiter.remain_post_attempt > 0:
            self.recruiter_persistent.reduce_remain_post_attempt(recruiter_id=self.user.recruiter.id)
        return ResponseModel(
            data=job_record.to_dict(), 
            detail="Success",
        ).model_dump(), HTTPStatus.OK
    
    def get_job_applicant_applied(self):
        jobs_applied = self.persistent.get_job_applied_by_applicant_id(self.user.applicant.id)
        result = [
            ApplicantJobPricing(
                **job_applied.to_dict(),
                job = OutputJob(
                    **job.to_dict(), 
                    category=CategoryDTO(**category.to_dict()),
                    poster=RecruiterDTO(
                        **poster.to_dict(),
                        information=UserInformation(
                            **poster_account.to_dict(),
                        )
                    )
                ),
            ).model_dump()
            for job_applied, job, category, poster, poster_account  in jobs_applied
        ]
        return ListResponseModel(
            detail="Success",
            data = result,
            total=len(result),
        ), HTTPStatus.OK
    
    def apply_job(self, job_id, job_apply: JobApply):
        job, status_code = self.get_job_by_id(job_id)
        if status_code != HTTPStatus.OK:
            return job, status_code
        elif job["data"]["status"] not in [JobStatus.OPEN, JobStatus.REOPEN]:
            return ResponseModel(
                detail="Job in progress cannot apply"
            ), HTTPStatus.BAD_REQUEST
 
        exist_pricing = self.persistent.get_job_apply_by_job_id_and_applicant_id(job_id, self.user.applicant.id)
        if exist_pricing:
            return ResponseModel(
                detail="Already applied"
            ), HTTPStatus.CONFLICT

        job_apply_data = JobApplyData(
            applicant_id = self.user.applicant.id,
            job_id = job_id,
            pricing = job_apply.pricing,
            experience_description = job_apply.experience_description,
            plan_description = job_apply.plan_description,
            status=JobPricingStatus.WAITING_FOR_APPROVE,
        )
        self.persistent.add_job_apply(job_apply_data)
        return ResponseModel(
            data=job_apply_data.to_dict(),
            detail="Success"
        ), HTTPStatus.CREATED
    
    def get_all_recruiter_jobs_posted(self):
        job_detail = self.persistent.get_all_jobs_by_recruiter_id(self.user.recruiter.id)
        result = [
            OutputJob(
                **job.to_dict(), 
                category=CategoryDTO(**category.to_dict()),
                poster=self.user.recruiter
            ) 
            for job, category  in job_detail
        ]
        return ListResponseModel(
            data=result,
            detail="Success",
            total=len(result)
        ).model_dump(), HTTPStatus.OK
    
    def get_all_recruiter_jobs_pricing_post(self, job_id):
        job_result, status = self.get_job_by_id(job_id)
        if status != HTTPStatus.OK:
            return job_result, status
        jobs_pricing = self.persistent.get_jobs_apply_by_job_id(job_id)
        result = [
            RecruiterJobPricing(
                job = OutputJob(**job_result["data"]),
                applicant=ApplicantDTO(
                    **applicant.to_dict(),
                    information=UserInformation(**account.to_dict())
                ),
                **job_apply.to_dict()
            )
            for job_apply, applicant, account in jobs_pricing
        ]
        return ListResponseModel(
            data=result,
            detail="Success",
            total=len(result)
        ).model_dump(), HTTPStatus.OK
        
    
    def change_job_apply_status(self, job_id, applicant_id, job_apply_status: JobApplyStatus):
        job_apply_info = self.persistent.get_job_apply_by_job_id_and_applicant_id(
            job_id,
            applicant_id
        )
        if not job_apply_info:
            return ResponseModel(
                detail="Not found pricing"
            ), HTTPStatus.NOT_FOUND
        
        job_apply, job, recruiter = job_apply_info
        if (
            recruiter.id != self.user.recruiter.id 
            or job_apply_status.status not in [JobPricingStatus.ACCEPTED, JobPricingStatus.DENY]
        ): 
            return ResponseModel(
                detail="Resource forbidden"
            ), HTTPStatus.FORBIDDEN
        
        if job_apply_status.status == JobPricingStatus.ACCEPTED:
            if job.status not in [JobStatus.OPEN, JobStatus.REOPEN]:
                return ResponseModel(
                    detail="Job in progress cannot change status"
                ), HTTPStatus.BAD_REQUEST
            for job_applied_detail in self.persistent.get_jobs_apply_by_job_id(job_id):
                job_applied = job_applied_detail[0]
                if job_applied.status == JobPricingStatus.ACCEPTED:
                    return ResponseModel(
                        detail="Another pricing have been applied"
                    ), HTTPStatus.CONFLICT
        elif job_apply.status == JobPricingStatus.ACCEPTED:
            return ResponseModel(
                detail="Cannot change status from ACCEPTED to DENY"
            ), HTTPStatus.BAD_REQUEST
        
        job_apply.status = job_apply_status.status
        self.persistent.add_job_apply(job_apply)
        if job_apply_status.status == JobPricingStatus.ACCEPTED:
            self.persistent.deny_all_waiting_job_apply(job_id)
            job.status = JobStatus.WORK_IN_PROGRESS
            self.persistent.add_job(job)

        return ResponseModel(
            data=job_apply.to_dict(),
            detail="Success"
        ).model_dump(), HTTPStatus.OK
        
