from sqlalchemy.orm.session import Session

class BasePersistent:
    def __init__(self, session):
        self.session: Session = session

    def commit_change(self):
        self.session.commit()