from models.data.Notification import Notification
from models.data.Applicant import Applicant
from models.data.Recruiter import Recruiter
from models.data.Account import Account
from sqlalchemy.orm.session import Session
from persistent.BasePersistent import BasePersistent

class NotificationPersistent(BasePersistent):
    def __init__(self, session: Session):
        super().__init__(session)

    def send_notification(self, notification):
        self.session.add(notification)
        self.session.commit()
        return notification
    
    def read_notification(self, notification_id):
        self.session.query(Notification).filter(
            Notification.id == notification_id
        ).update({"is_read": True}, synchronize_session=False)
        self.session.commit()

    def bulk_read_notification(self, receiver_id):
        self.session.query(Notification).filter(
            Notification.receiver_id == receiver_id,
            Notification.is_read.is_(False),
        ).update({"is_read": True}, synchronize_session=False)
        self.session.commit()

    def bulk_insert_notification(self, list_notification):
        self.session.bulk_save_objects(list_notification)
        self.session.commit()

    def get_account_by_applicant_id(self, applicant_id):
        return self.session.query(Account).filter(
            Applicant.id == applicant_id,
            Account.id == Applicant.account_id
        ).first()
    
    def get_list_account_by_list_applicant_id(self, list_applicant_id):
        return self.session.query(Account).filter(
            Applicant.id.in_(list_applicant_id),
            Account.id == Applicant.account_id 
        ).all()
    
    def get_recruiter_by_applicant_id(self, recruiter_id):
        return self.session.query(Account).filter(
            Recruiter.id == recruiter_id,
            Account.id == Recruiter.account_id 
        ).first()
    
    def get_notification_by_user_id(self, user_id):
        self.session.rollback()
        return self.session.query(Notification).filter(
            Notification.receiver_id == user_id 
        ).order_by(Notification.created_at.desc()).all()