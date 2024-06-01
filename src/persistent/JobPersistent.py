from uuid import uuid4
from models.data.Job import Job
from models.data.JobApply import JobApply
from models.data.Category import Category
from models.data.Recruiter import Recruiter
from models.data.Applicant import Applicant
from models.data.Account import Account
from sqlalchemy.orm.session import Session
from sqlalchemy import and_
from common.helper import get_filters, parse_order_by
from common.constant import JobStatus, JobPricingStatus

class JobPersistent:
    def __init__(self, session):
        self.session: Session = session
    
    def get_all_jobs(self, params):
        query = self.session.query(
            Job,
            Category,
            Recruiter,
            Account,
        ).filter(
            Category.id == Job.category_id,
            Recruiter.id == Job.poster_id,
            Account.id == Recruiter.account_id
        )
        filters = get_filters(params, Job)
        if filters:
            query = query.filter(and_(*filters))
        order_criteria = parse_order_by(params, Job)
        for key, direction in order_criteria:
            column = getattr(Job, key)
            if direction == "asc":
                query = query.order_by(column.asc())
            else:
                query = query.order_by(column.desc())
        return query.all()
    
    def get_job_by_id(self, job_id):
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
    
    def add_job_apply(self, job_apply):
        self.session.add(job_apply)
        self.session.commit()
        return job_apply
    
    def get_jobs_apply_by_job_id(self, job_id):
        return self.session.query(JobApply, Applicant, Account).filter(
            JobApply.job_id == job_id,
            Applicant.id == JobApply.applicant_id,
            Account.id == Applicant.account_id,
        ).all()
    
    def get_job_apply_by_job_id_and_applicant_id(self, job_id, applicant_id):
        return self.session.query(
            JobApply,
            Job,
            Recruiter,
        ).filter(
            JobApply.applicant_id == applicant_id,
            JobApply.job_id == job_id,
            Job.id == JobApply.job_id,
            Recruiter.id == Job.poster_id,
        ).first()
    
    def get_all_jobs_by_recruiter_id(self, recruiter_id):
        return self.session.query(
            Job,
            Category,
        ).filter(
            Category.id == Job.category_id,
            Job.poster_id == recruiter_id
        ).all()
    
    def deny_all_waiting_job_apply(self, job_id):
        self.session.query(JobApply).filter(
            JobApply.job_id == job_id,
            JobApply.status == JobPricingStatus.WAITING_FOR_APPROVE,
        ).update({"status": JobStatus.DENY})