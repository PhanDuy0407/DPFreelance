from uuid import uuid4
from models.data.Recruiter import Recruiter
from models.data.Job import Job
from models.data.JobApply import JobApply
from models.data.Account import Account
from sqlalchemy.orm.session import Session
from persistent.BasePersistent import BasePersistent
from sqlalchemy import func, case
from common.constant import JobApplyStatus, JobStatus

class RecruiterPersistent(BasePersistent):
    
    def get_all_recruiters(self):
        return self.session.query(Recruiter, Account).filter(
            Recruiter.account_id == Account.id
        ).order_by(Recruiter.created_at.desc()).all()
    
    def get_recruiter_by_id(self, recruiter_id):
        return self.session.query(Recruiter, Account).filter(
            Recruiter.id == recruiter_id,
            Recruiter.account_id == Account.id
        ).first()
    
    def get_recruiter_by_account_id(self, account_id):
        return self.session.query(Recruiter).filter(
            Recruiter.account_id == account_id
        ).first()
    
    def add_recruiter(self, recruiter):
        self.session.add(recruiter)
        self.session.commit()
        return recruiter
    
    def reduce_remain_post_attempt(self, recruiter_id):
        recruiter = self.session.query(Recruiter).filter(Recruiter.id == recruiter_id).first()
        if not recruiter:
            return False
        
        recruiter.remain_post_attempt = recruiter.remain_post_attempt - 1 if recruiter.remain_post_attempt > 1 else 0
        self.session.commit()
        return recruiter
    
    def reset_free_post_attempt(self, recruiter_id):
        recruiter = self.session.query(Recruiter).filter(Recruiter.id == recruiter_id).first()
        if not recruiter:
            return False
        
        recruiter.free_post_attempt = 0
        self.session.commit()
        return recruiter
    
    def get_recruiter_statistic_by_id(self, recruiter_id):
        job_posted = len(self.session.query(
            Job.id
        ).filter(
            Job.poster_id == recruiter_id,
            Job.status.notin_([JobStatus.DENY, JobStatus.WAITING_FOR_APPROVE])
        ).all())
        
        job_done, job_in_progress = self.session.query(
            func.count(case((JobApply.status == JobApplyStatus.DONE, 1), else_=None)).label('job_done'),
            func.count(case((JobApply.status == JobApplyStatus.ACCEPTED, 1), else_=None)).label('job_in_progress'),
        ).filter(
            JobApply.job_id == Job.id,
            Job.poster_id == recruiter_id
        ).first()

        return job_posted, job_done, job_in_progress
    
    def get_recruiter_by_phone(self, phone):
        return self.session.query(Recruiter).filter(
            Recruiter.phone == phone
        ).first()
    
    def get_recruiter_by_cccd(self, cccd):
        return self.session.query(Recruiter).filter(
            Recruiter.cccd == cccd
        ).first()
