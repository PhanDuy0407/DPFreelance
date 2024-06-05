from uuid import uuid4
from models.data.Applicant import Applicant
from models.data.Account import Account
from sqlalchemy.orm.session import Session
from persistent.BasePersistent import BasePersistent

class ApplicantPersistent(BasePersistent):
    
    def get_all_applicants(self):
        return self.session.query(
            Applicant, Account
        ).filter(Applicant.account_id == Account.id).all()
    
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