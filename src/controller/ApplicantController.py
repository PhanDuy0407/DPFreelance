from uuid import uuid4
from http import HTTPStatus
from datetime import datetime

from persistent.ApplicantPersistent import ApplicantPersistent
from persistent.JobPersistent import JobPersistent
from models.dto.output.ApplicantDTO import ApplicantDTO as OutputApplicant, ApplicantStatistic
from models.dto.input.Applicant import Applicant as InputApplicant
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
            detail="Thành công",
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
            detail="Thành công",
        ).model_dump(), HTTPStatus.OK
    
    def register(self, applicant_info: InputApplicant):
        if self.user.applicant:
            return ResponseModel(
                detail="Tài khản đã là người tìm việc"
            ), HTTPStatus.CONFLICT
        
        exist = self.persistent.get_applicant_by_phone(applicant_info.phone)
        if exist:
            return ResponseModel(
                detail="Số điện thoại đã được sử dụng"
            ), HTTPStatus.CONFLICT
        
        applicant = Applicant(
            id = uuid4(),
            account_id = self.user.id,
            bio = applicant_info.bio,
            city = applicant_info.city,
            address = applicant_info.address,
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
            detail="Thành công"
        ), HTTPStatus.CREATED
    
    def get_applicant_statistic_by_id(self, applicant_id):
        if not self.persistent.get_applicant_by_id(applicant_id):
            return ResponseModel(
                detail="Applicant not found"
            ), HTTPStatus.NOT_FOUND
        statistics = self.persistent.get_applicant_statistics_by_id(applicant_id)
        return ResponseModel(
            data=ApplicantStatistic(
                job_apply=statistics[0],
                job_done=statistics[1],
                job_in_progress=statistics[2]
            ),
            detail="Thành công"
        ), HTTPStatus.OK