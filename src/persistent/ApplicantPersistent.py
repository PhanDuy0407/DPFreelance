from uuid import uuid4
from models.data.Applicant import Applicant
from models.data.Account import Account
from sqlalchemy.orm.session import Session
from persistent.BasePersistent import BasePersistent
from models.data.JobApply import JobApply
from sqlalchemy import func, case

class ApplicantPersistent(BasePersistent):
    
    def get_all_applicants(self):
        return self.session.query(
            Applicant, Account
        ).filter(Applicant.account_id == Account.id).order_by(
            Applicant.created_at.desc()
        ).all()
    
    def get_applicant_by_id(self, applicant_id):
        return self.session.query(Applicant, Account).filter(
            Applicant.id == applicant_id,
            Account.id == Applicant.account_id,
        ).first()
    
    def get_applicant_by_account_id(self, account_id):
        return self.session.query(Applicant).filter(
            Applicant.account_id == account_id
        ).first()
    
    def add_applicant(self, applicant):
        self.session.add(applicant)
        self.session.commit()
        return applicant
    
    def get_applicant_by_phone(self, phone):
        return self.session.query(Applicant).filter(
            Applicant.phone == phone
        ).first()
    
    def get_applicant_statistics_by_id(self, applicant_id):
        return self.session.query(
            func.count(JobApply.job_id).label("job_apply"),
            func.count(case((JobApply.status == 'DONE', 1), else_=None)).label('job_done'),
            func.count(case((JobApply.status == "ACCEPTED", 1), else_=None)).label('job_in_progress'),
        ).filter(
            JobApply.applicant_id == applicant_id
        ).first()