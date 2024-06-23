from http import HTTPStatus

from persistent.CategoryPersistent import CategoryPersistent
from models.dto.output.CategoryDTO import CategoryDTO
from models.dto.output.AccountDTO import Account
from controller.model.ResponseModel import ListResponseModel

class CategoryController:
    def __init__(self, user: Account, session) -> None:
        self.user = user
        self.persistent = CategoryPersistent(session)

    def get_all_category(self):
        list_category = self.persistent.get_all_category()
        result = [
            CategoryDTO(**category.to_dict())
            for category  in list_category
        ]
        return ListResponseModel(
            data=result,
            detail="Thành công",
            total=len(result)
        ).model_dump(), HTTPStatus.OK