from enum import Enum
ADMIN_ROLE = "Admin"
RECRUITER_ROLE = "Recruiter"
APPLICANT_ROLE = "Applicant"

class JobStatus(Enum):
    WAITING_FOR_APPROVE = "WAITING_FOR_APPROVE"
    OPEN = "OPEN"
    DENY = "DENY"
    REOPEN = "REOPEN"
    WORK_IN_PROGRESS = "WORK_IN_PROGRESS"

    