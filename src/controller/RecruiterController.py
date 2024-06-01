from http import HTTPStatus
from uuid import uuid4
from datetime import datetime

from persistent.RecruiterPersistent import RecruiterPersistent
from persistent.JobPersistent import JobPersistent
from models.dto.output.RecruiterDTO import RecruiterDTO
from models.dto.input.Recruiter import Recruiter as InputRecruiter
from models.dto.output.UserInformation import UserInformation
from models.dto.output.AccountDTO import Account
from models.data.Recruiter import Recruiter
from controller.model.ResponseModel import ListResponseModel, ResponseModel

class RecruiterController:
    def __init__(self, user: Account, session) -> None:
        self.user = user
        self.persistent = RecruiterPersistent(session)
        self.job_persistent = JobPersistent(session)

    def get_all_recruiters(self):
        recruiters = self.persistent.get_all_recruiters()
        result = [
            RecruiterDTO(
                **recruiter.to_dict(),
                information=UserInformation(
                    **account.to_dict()
                )
            )
            for recruiter, account in recruiters
        ]
        return ListResponseModel(
            data=result,
            detail="Success",
            total=len(result)
        ).model_dump(), HTTPStatus.OK
    
    def get_recruiter_detail(self, recruiter_id):
        recruiter_info = self.persistent.get_recruiter_by_id(recruiter_id)
        if not recruiter_info:
            return ResponseModel(
                detail="Recruiter not found"
            ).model_dump(), HTTPStatus.NOT_FOUND

        recruiter, account = recruiter_info
        return ResponseModel(
            data=RecruiterDTO(
                **recruiter.to_dict(),
                information=UserInformation(
                    **account.to_dict()
                )
            ),
            detail="Success"
        ).model_dump(), HTTPStatus.OK
    
    def register(self, recruiter_info: InputRecruiter):
        if self.user.recruiter:
            return ResponseModel(
                detail="Account already register as an Recruiter"
            ), HTTPStatus.CONFLICT
        
        recruiter = Recruiter(
            id = uuid4(),
            account_id = self.user.id,
            recruiter_email = recruiter_info.recruiter_email,
            phone = recruiter_info.phone,
            free_post_attempt = 1,
            remain_post_attempt = 0,
            created_at = datetime.now(),
            updated_at = datetime.now()
        )

        self.persistent.add_recruiter(recruiter)
        return ResponseModel(
            data=recruiter.to_dict(),
            detail="Success"
        ), HTTPStatus.CREATED