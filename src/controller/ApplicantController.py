from uuid import uuid4
from http import HTTPStatus
from datetime import datetime

from persistent.ApplicantPersistent import ApplicantPersistent
from persistent.JobPersistent import JobPersistent
from models.dto.output.ApplicantDTO import ApplicantDTO as OutputApplicant
from models.dto.input.Applicant import Applicant as InputApplicant
from models.dto.output.JobDTO import JobDTO
from models.dto.output.CategoryDTO import CategoryDTO
from models.dto.output.RecruiterDTO import RecruiterDTO
from models.dto.output.JobApplyDTO import JobApplyDTO
from models.dto.output.UserInformation import UserInformation
from models.data.Applicant import Applicant
from controller.model.ResponseModel import ListResponseModel, ResponseModel

class ApplicantController:
    def __init__(self, user, session) -> None:
        self.user = user
        self.persistent = ApplicantPersistent(session)
        self.job_persistent = JobPersistent(session)

    def get_all_applicants(self):
        applicants = self.persistent.get_all_applicants()
        result = [
            OutputApplicant(
                **applicant.to_dict(),
                information=UserInformation(**account.to_dict())
            )
            for applicant, account in applicants
        ]
        return ListResponseModel(
            data=result,
            detail="Success",
            total=len(result)
        ).model_dump(), HTTPStatus.OK
    
    def get_applicant_by_id(self, applicant_id):
        applicant_info = self.persistent.get_applicant_by_id(applicant_id)
        if not applicant_info:
            return ResponseModel(
                detail="Applicant not found"
            ), HTTPStatus.NOT_FOUND

        applicant, account = applicant_info
        return ResponseModel(
            data=OutputApplicant(
                **applicant.to_dict(),
                information=UserInformation(**account.to_dict())
            ),
            detail="Success",
        ).model_dump(), HTTPStatus.OK
    
    def get_job_applied(self):
        applicant = self.persistent.get_applicant_by_account_id(self.user.id)
        if not applicant:
            return ResponseModel(
                detail="Applicant not found"
            ), HTTPStatus.NOT_FOUND

        jobs_applied = self.job_persistent.get_job_applied_by_applicant_id(applicant.id)
        result = [
            JobApplyDTO(
                **job_applied.to_dict(),
                job = JobDTO(
                    **job.to_dict(), 
                    category=CategoryDTO(**category.to_dict()),
                    poster=RecruiterDTO(
                        **poster.to_dict(),
                        information=UserInformation(
                            **poster_account.to_dict(),
                        )
                    )
                )
            ).model_dump()
            for job_applied, job, category, poster, poster_account  in jobs_applied
        ]
        return ListResponseModel(
            detail="Success",
            data = result,
            total=len(result),
        ), HTTPStatus.OK
    
    def register(self, applicant_info: InputApplicant):
        if self.user.applicant:
            return ResponseModel(
                detail="Account already register as an Applicant"
            ), HTTPStatus.CONFLICT
        
        applicant = Applicant(
            id = uuid4(),
            account_id = self.user.id,
            bio = applicant_info.bio,
            skills = applicant_info.skills,
            phone = applicant_info.phone,
            work_time = applicant_info.work_time,
            cv_link = applicant_info.cv_link,
            created_at = datetime.now(),
            updated_at = datetime.now()
        )

        self.persistent.add_applicant(applicant)
        return ResponseModel(
            data=applicant.to_dict(),
            detail="Success"
        ), HTTPStatus.CREATED
        
