from models.dto.output.JobApplyDTO import JobApplyDTO
from models.dto.output.ApplicantDTO import ApplicantDTO
from models.dto.output.JobDTO import JobDTO

class AdminJob(JobApplyDTO):
    applicant: ApplicantDTO
    job: JobDTO