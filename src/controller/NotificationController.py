from uuid import uuid4
import json
from http import HTTPStatus
from models.data.Notification import Notification

from persistent.NotificationPersistent import NotificationPersistent
from controller.model.ResponseModel import ListResponseModel
from models.dto.output.NotificationDTO import NotificationDTO
from common.helper import custom_encoder

class NotificationController:
    def __init__(self, user, session) -> None:
        self.user = user
        self.persistent = NotificationPersistent(session)

    def action(self, data):
        action = data.get("action")
        if action == "get_notifications":
            return self.get_all_notifications()
        if action == "read_notification":
            return self.read_notification(data.get("resource"))
        if action == "bulk_read_notifications":
            return self.bulk_read_notification()

    def get_all_notifications(self):
        notifications = self.persistent.get_notification_by_user_id(self.user.id)
        result = [
            NotificationDTO(**notification.to_dict())
            for notification in notifications
        ]
        return json.loads(json.dumps(
            ListResponseModel(
                data=result,
                detail="Success",
                total=len(result)
            ).model_dump(),
            default=custom_encoder,
        ))

    def send_notification_to_applicant(self, applicant_id, content, nav_link, avatar = None):
        account = self.persistent.get_account_by_applicant_id(applicant_id)
        if account:
            noti_data = Notification(
                id = uuid4(),
                receiver_id = account.id,
                content = content,
                nav_link = nav_link,
                avatar=avatar,
            )
            self.persistent.send_notification(noti_data)

    def bulk_insert_notification_applicant(self, list_applicant_id, content, nav_link, avatar = None):
        list_receiver = self.persistent.get_list_account_by_list_applicant_id(list_applicant_id)
        list_notification = [
            Notification(
                id = uuid4(),
                receiver_id = receiver.id,
                content = content,
                nav_link = nav_link,
                avatar = avatar,
            ) for receiver in list_receiver
        ]
        self.persistent.bulk_insert_notification(list_notification)

    def send_notification_to_recruiter(self, recruiter_id, content, nav_link, avatar = None):
        account = self.persistent.get_recruiter_by_applicant_id(recruiter_id)
        if account:
            noti_data = Notification(
                id = uuid4(),
                receiver_id = account.id,
                content = content,
                nav_link = nav_link,
                avatar = avatar,
            )
            self.persistent.send_notification(noti_data)

    def read_notification(self, notification_id):
        self.persistent.read_notification(notification_id)
        return self.get_all_notifications()
    
    def bulk_read_notification(self):
        self.persistent.bulk_read_notification(self.user.id)
        return self.get_all_notifications()
