import uuid
from http import HTTPStatus
from datetime import datetime

from persistent.JobPersistent import JobPersistent
from persistent.RecruiterPersistent import RecruiterPersistent
from models.dto.output.JobDTO import JobDTO as OutputJob, RecruiterJobDTO as OutputRecruiterJob
from models.dto.output.RecruiterJob import RecruiterJob
from models.dto.output.AdminJob import AdminJob
from models.dto.output.ApplicantJob import ApplicantJob
from models.dto.input.Job import Job as InputJob
from models.dto.input.ApplyStatus import ApplyStatus
from models.dto.output.RecruiterDTO import RecruiterDTO
from models.dto.output.ApplicantDTO import ApplicantDTO
from models.dto.output.UserInformation import UserInformation
from models.dto.output.CategoryDTO import CategoryDTO
from models.dto.output.AccountDTO import Account
from models.data.Job import Job
from models.data.JobApply import JobApply as JobApplyData
from controller.model.ResponseModel import ListResponseModel, ResponseModel
from common.constant import JobApplyStatus, JobStatus
from controller.NotificationController import NotificationController

class JobController:
    def __init__(self, user: Account, session) -> None:
        self.user = user
        self.persistent = JobPersistent(session)
        self.recruiter_persistent = RecruiterPersistent(session)
        self.notification = NotificationController(user, session)

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
                ),
                number_of_applied=number_of_applied,
            ) 
            for job, category, poster, poster_account, number_of_applied  in job_detail
        ]
        return ListResponseModel(
            data=result,
            detail="Thành công",
            total=len(result)
        ).model_dump(), HTTPStatus.OK
    
    def get_job_by_id(self, job_id):
        job_detail = self.persistent.get_job_by_id(job_id)
        if not job_detail:
            return ResponseModel(
                detail="Job not found"
            ), HTTPStatus.NOT_FOUND

        job, category, poster, poster_account, number_of_applied = job_detail
        return ResponseModel(
            data=OutputJob(
                **job.to_dict(), 
                category=CategoryDTO(**category.to_dict()),
                poster=RecruiterDTO(
                    **poster.to_dict(),
                    information=UserInformation(
                        **poster_account.to_dict(),
                    )
                ),
                number_of_applied=number_of_applied,
            ),
            detail="Thành công",
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
            min_price=job.min_price,
            max_price=job.max_price,
            price_unit=job.price_unit,
            require_skills=job.require_skills,
            type=job.type,
            status=JobStatus.WAITING_FOR_APPROVE,
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
            detail="Thành công",
        ).model_dump(), HTTPStatus.OK
    
    def get_job_applicant_applied(self, params):
        jobs_applied = self.persistent.get_job_applied_by_applicant_id(self.user.applicant.id, params)
        result = [
            ApplicantJob(
                **job_applied.to_dict(),
                job = OutputJob(
                    **job.to_dict(), 
                    category=CategoryDTO(**category.to_dict()),
                    poster=RecruiterDTO(
                        **poster.to_dict(),
                        information=UserInformation(
                            **poster_account.to_dict(),
                        )
                    ),
                    number_of_applied=number_of_applied
                ),
            ).model_dump()
            for job_applied, job, category, poster, poster_account, number_of_applied in jobs_applied
        ]
        return ListResponseModel(
            detail="Thành công",
            data = result,
            total=len(result),
        ), HTTPStatus.OK
    
    def edit_job(self, job_id, input_job: InputJob):
        job_detail = self.persistent.get_job_by_id(job_id)
        if not job_detail:
            return ResponseModel(
                detail="Job not found"
            ), HTTPStatus.NOT_FOUND
        
        job, _, _, _, _ = job_detail
        if job.status != JobStatus.WAITING_FOR_APPROVE:
            return ResponseModel(
                detail=f"Không thể cập nhật tin tuyển dụng với trạng thái {job.status}"
            ), HTTPStatus.CONFLICT

        self.persistent.edit_job(job_id, input_job.model_dump(exclude_none=True))
        return ResponseModel(
            detail="Thành công",
        ), HTTPStatus.OK

    
    def apply_job(self, job_id):
        job, status_code = self.get_job_by_id(job_id)
        if status_code != HTTPStatus.OK:
            return job, status_code
        elif job["data"]["status"] not in [JobStatus.OPEN, JobStatus.REOPEN]:
            return ResponseModel(
                detail="Job in progress cannot apply"
            ), HTTPStatus.BAD_REQUEST
 
        exist_apply = self.persistent.get_job_apply_by_job_id_and_applicant_id(job_id, self.user.applicant.id)
        if exist_apply:
            return ResponseModel(
                detail="Already applied"
            ), HTTPStatus.CONFLICT

        job_apply_data = JobApplyData(
            applicant_id = self.user.applicant.id,
            job_id = job_id,
            status=JobApplyStatus.WAITING_FOR_APPROVE,
        )
        self.persistent.add_job_apply(job_apply_data)
        job_name = job["data"]["name"]
        self.notification.send_notification_to_recruiter(
            recruiter_id=job.get("data", {}).get("poster", {}).get("id"),
            content=f"<strong>{self.user.fname} {self.user.lname}</strong> đã ứng tuyển công việc <strong>{job_name}</strong> của bạn",
            nav_link=f"recruiters/jobs/{job_id}",
            avatar=self.user.avatar,
        )
        return ResponseModel(
            data=job_apply_data.to_dict(),
            detail="Thành công"
        ), HTTPStatus.CREATED
    
    def revoke_job_apply(self, job_id):
        exist_job_apply = self.persistent.get_job_apply_by_job_id_and_applicant_id(job_id, self.user.applicant.id)
        if not exist_job_apply:
            return ResponseModel(
                detail="Job apply not found"
            ), HTTPStatus.NOT_FOUND
        job_apply, job, _ = exist_job_apply
        if not job_apply.status == JobApplyStatus.ACCEPTED:
            return ResponseModel(
                detail=f"Cannot revoke job apply with status {job_apply.status}"
            ), HTTPStatus.CONFLICT
        job_apply.status = JobApplyStatus.REVOKE
        job.status = JobStatus.OPEN
        self.persistent.commit_change()
        return ResponseModel(
            detail="Thành công"
        ), HTTPStatus.OK
    
    def get_all_recruiter_jobs_posted(self, params):
        job_detail = self.persistent.get_all_jobs_by_recruiter_id(self.user.recruiter.id, params)
        result = []
        for job, category, number_of_applied in job_detail:
            job_applied = None
            if params.get("apply_status"):
                job_applied_detail=self.persistent.get_job_applied_success_by_job_id(job.id, params.get("apply_status"))
                if job_applied_detail:
                    job_apply, applicant, account = job_applied_detail
                    job_applied = RecruiterJob(
                        applicant=ApplicantDTO(
                            **applicant.to_dict(),
                            information=UserInformation(**account.to_dict())
                        ),
                        **job_apply.to_dict()
                    )
                else:
                    continue
            result.append(
                OutputRecruiterJob(
                    **job.to_dict(), 
                    category=CategoryDTO(**category.to_dict()),
                    poster=self.user.recruiter,
                    number_of_applied=number_of_applied,
                    job_applied=job_applied
                )
            )
        return ListResponseModel(
            data=result,
            detail="Thành công",
            total=len(result)
        ).model_dump(), HTTPStatus.OK
    
    def get_all_recruiter_jobs_apply(self, job_id):
        job_result, status = self.get_job_by_id(job_id)
        if status != HTTPStatus.OK:
            return job_result, status
        poster_id = job_result.get("data", {}).get("poster", {}).get("id")
        if poster_id != self.user.recruiter.id:
            return ResponseModel(
                detail="Resource forbidden"
            ), HTTPStatus.FORBIDDEN
        jobs_pricing = self.persistent.get_jobs_apply_by_job_id(job_id)
        result = [
            RecruiterJob(
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
            detail="Thành công",
            total=len(result)
        ).model_dump(), HTTPStatus.OK
        
    
    def change_job_apply_status(self, job_id, applicant_id, job_apply_status: ApplyStatus):
        job_apply_info = self.persistent.get_job_apply_by_job_id_and_applicant_id(
            job_id,
            applicant_id
        )
        if not job_apply_info:
            return ResponseModel(
                detail="Ứng viên chưa ứng tuyển công việc này"
            ), HTTPStatus.NOT_FOUND
        
        job_apply, job, recruiter = job_apply_info
        if (
            recruiter.id != self.user.recruiter.id 
            or job_apply_status.status not in [JobApplyStatus.ACCEPTED, JobApplyStatus.DENY]
        ): 
            return ResponseModel(
                detail="Bạn không có quyền thay đổi trạng thái tin tuyển dụng này"
            ), HTTPStatus.FORBIDDEN
        
        if job_apply_status.status == JobApplyStatus.ACCEPTED:
            if job.status not in [JobStatus.OPEN, JobStatus.REOPEN]:
                return ResponseModel(
                    detail=f"Không thể tuyển ứng viên vì tin tuyển dụng có trạng thái {job.status}"
                ), HTTPStatus.BAD_REQUEST
        elif job_apply.status == JobApplyStatus.ACCEPTED:
            return ResponseModel(
                detail="Cannot change status from ACCEPTED to DENY"
            ), HTTPStatus.BAD_REQUEST
        
        job_apply.status = job_apply_status.status
        if job_apply_status.status == JobApplyStatus.ACCEPTED:
            job_apply.applied_at = datetime.now()
            self.notification.send_notification_to_applicant(
                applicant_id=applicant_id,
                content=f"Đơn ứng tuyển của bạn cho công việc <strong>{job.name}</strong> đã được chấp thuận",
                nav_link=f"jobs/{job_id}",
                avatar=self.user.avatar,
            )
            job_denied = self.persistent.deny_all_waiting_job_apply(job_id)
            self.notification.bulk_insert_notification_applicant(
                list_applicant_id=[data.applicant_id for data in job_denied],
                content=f"Đơn ứng tuyển của bạn cho công việc <strong>{job.name}</strong> đã bị từ chối",
                nav_link=f"jobs/{job_id}",
                avatar=self.user.avatar,
            )
            job.status = JobStatus.DONE
        if job_apply_status.status == JobApplyStatus.DENY:
            self.notification.send_notification_to_applicant(
                applicant_id=applicant_id,
                content=f"Đơn ứng tuyển của bạn cho công việc <strong>{job.name}</strong> đã bị từ chối",
                nav_link=f"jobs/{job_id}",
                avatar=self.user.avatar,
            )
        self.persistent.commit_change()

        return ResponseModel(
            data=job_apply.to_dict(),
            detail="Thành công"
        ).model_dump(), HTTPStatus.OK
    
    def get_all_job_applies_success(self, params):
        jobs_applied = self.persistent.get_all_job_applies_success(params)
        result = [
            AdminJob(
                **job_applied.to_dict(),
                job = OutputJob(
                    **job.to_dict(), 
                    category=CategoryDTO(**category.to_dict()),
                    poster=RecruiterDTO(
                        **poster.to_dict(),
                        information=UserInformation(
                            **poster_account.to_dict(),
                        )
                    ),
                    number_of_applied=number_of_applied
                ),
                applicant=ApplicantDTO(
                    **applicant.to_dict(),
                    information=UserInformation(
                        **applicant_account.to_dict(),
                    )
                )
            ).model_dump()
            for job_applied, job, category, applicant, applicant_account, poster, poster_account, number_of_applied in jobs_applied
        ]
        return ListResponseModel(
            detail="Thành công",
            data = result,
            total=len(result),
        ), HTTPStatus.OK
    
    def recruiter_mark_done_job(self, job_id):
        job = self.persistent.get_job_by_id(job_id)
        if not job:
            return ResponseModel(
                detail="Không tìm thấy công việc"
            ), HTTPStatus.NOT_FOUND

        job_applied_detail=self.persistent.get_job_applied_success_by_job_id(job_id, JobApplyStatus.ACCEPTED)
        if not job_applied_detail:
            return ResponseModel(
                detail="Công việc chưa được thực hiện"
            ), HTTPStatus.CONFLICT
        job_apply, applicant, _ = job_applied_detail
        job = job[0]

        job_apply.status = JobApplyStatus.DONE
        self.persistent.commit_change()
        self.notification.send_notification_to_applicant(
            applicant_id=applicant.id,
            content=f"Công việc <strong>{job.name}</strong> của bạn đã được đánh giá là: Hoàn thành",
            nav_link=f"applicants/jobs",
            avatar=self.user.avatar,
        )

        return ResponseModel(
            detail="Thành công",
        ).model_dump(), HTTPStatus.OK