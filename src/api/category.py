from common.database_connection import get_db
from common.helper import get_current_user
from fastapi import APIRouter, Depends, Response
from controller.CategoryController import CategoryController

router = APIRouter(prefix="/api/v1/category", tags=["category"])

@router.get("")
async def list(response_model: Response, user = Depends(get_current_user()), session = Depends(get_db)):
    controller = CategoryController(user, session)
    result, status_code = controller.get_all_category()
    response_model.status_code = status_code
    return result