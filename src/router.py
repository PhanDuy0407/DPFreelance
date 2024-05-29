from api.auth import router as auth
from api.applicant import router as applicant
from api.job import router as job
from api.category import router as category
from api.recruiter import router as recruiter

routers = [
    auth,
    applicant,
    job,
    category,
    recruiter
]