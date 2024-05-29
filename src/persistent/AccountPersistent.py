from uuid import uuid4
from models.data.Account import Account
from sqlalchemy.orm.session import Session
from sqlalchemy import or_

class AccountPersistent:
    def __init__(self, session):
        self.session: Session = session
    
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