from uuid import uuid4
from models.data.Job import Job
from models.data.JobApply import JobApply
from models.data.Category import Category
from models.data.Recruiter import Recruiter
from models.data.Account import Account
from sqlalchemy.orm.session import Session

class JobPersistent:
    def __init__(self, session):
        self.session: Session = session
    
    def get_all_jobs(self):
        return self.session.query(
            Job,
            Category,
            Recruiter,
            Account,
        ).filter(
            Category.id == Job.category_id,
            Recruiter.id == Job.poster_id,
            Account.id == Recruiter.account_id
        ).all()
    
    def get_jobs_by_id(self, job_id):
        return self.session.query(
            Job,
            Category,
            Recruiter,
            Account,
        ).filter(
            Job.id == job_id,
            Category.id == Job.category_id,
            Recruiter.id == Job.poster_id,
            Account.id == Recruiter.account_id
        ).first()
    
    def get_job_applied_by_applicant_id(self, applicant_id):
        return self.session.query(
            JobApply,
            Job,
            Category,
            Recruiter,
            Account,
        ).filter(
            JobApply.applicant_id == applicant_id,
            Job.id == JobApply.job_id,
            Category.id == Job.category_id,
            Recruiter.id == Job.poster_id,
            Account.id == Recruiter.account_id
        ).all()
    
    def add_job(self, job):
        self.session.add(job)
        self.session.commit()
        return job