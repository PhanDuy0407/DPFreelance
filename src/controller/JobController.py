import uuid
from http import HTTPStatus
from datetime import datetime, timedelta

from persistent.JobPersistent import JobPersistent
from persistent.RecruiterPersistent import RecruiterPersistent
from models.dto.output.JobDTO import JobDTO as OutputJob
from models.dto.input.Job import Job as InputJob
from models.dto.output.RecruiterDTO import RecruiterDTO
from models.dto.output.UserInformation import UserInformation
from models.dto.output.CategoryDTO import CategoryDTO
from models.dto.output.AccountDTO import Account
from models.data.Job import Job
from controller.model.ResponseModel import ListResponseModel, ResponseModel

class JobController:
    def __init__(self, user: Account, session) -> None:
        self.user = user
        self.persistent = JobPersistent(session)
        self.recruiter_persistent = RecruiterPersistent(session)

    def get_all_jobs(self):
        job_detail = self.persistent.get_all_jobs()
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
        job_detail = self.persistent.get_jobs_by_id(job_id)
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
