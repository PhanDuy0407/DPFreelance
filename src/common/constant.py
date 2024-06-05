from enum import Enum
ADMIN_ROLE = "Admin"
RECRUITER_ROLE = "Recruiter"
APPLICANT_ROLE = "Applicant"

class JobStatus:
    WAITING_FOR_APPROVE = "WAITING_FOR_APPROVE"
    OPEN = "OPEN"
    DENY = "DENY"
    REOPEN = "REOPEN"
    WORK_IN_PROGRESS = "WORK_IN_PROGRESS"
    CLOSED = "CLOSED"
    DONE = "DONE"

class JobPricingStatus:
    WAITING_FOR_APPROVE = "WAITING_FOR_APPROVE"
    DENY = "DENY"
    ACCEPTED = "ACCEPTED"
    REVOKE = "REVOKE"
    DONE = "DONE"

    