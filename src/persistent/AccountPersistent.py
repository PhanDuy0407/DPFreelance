from uuid import uuid4
from models.data.Account import Account
from models.data.Applicant import Applicant
from models.data.Recruiter import Recruiter
from sqlalchemy.orm.session import Session
from sqlalchemy import or_
from persistent.BasePersistent import BasePersistent

class AccountPersistent(BasePersistent):
    
    def get_account_by_id(self, account_id):
        return self.session.query(Account).filter(
            Account.id == account_id
        ).first()
    
    def get_account_by_username(self, username):
        return self.session.query(Account).filter(
            Account.username == username
        ).first()
    
    def is_username_or_email_exist(self, username = None, email = None):
        return self.session.query(Account).filter(
            or_(Account.username == username, Account.email == email)
        ).first() is not None
    
    def create_account(self, username, password, email = None, fname = None, lname = None):
        account = Account(
            id=str(uuid4()),
            username=username,
            password=password,
            email=email,
            fname=fname,
            lname=lname
        )
        self.session.add(account)
        self.session.commit()
        return account
    
    def get_all_account(self):
        return self.session.query(Account, Applicant, Recruiter).outerjoin(
            Applicant, Account.id == Applicant.account_id
        ).outerjoin(
            Recruiter, Account.id == Recruiter.account_id,
        ).order_by(Account.created_at.desc()).all()
    
    def toggle_account(self, account_id, enable):
        self.session.query(Account).filter(
            Account.id == account_id
        ).update({"enable": enable}, synchronize_session=False)
        self.commit_change()