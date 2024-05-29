from uuid import uuid4
from models.data.Recruiter import Recruiter
from models.data.Account import Account
from sqlalchemy.orm.session import Session

class RecruiterPersistent:
    def __init__(self, session):
        self.session: Session = session
    
    def get_all_recruiters(self):
        return self.session.query(Recruiter, Account).filter(
            Recruiter.account_id == Account.id
        ).all()
    
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
