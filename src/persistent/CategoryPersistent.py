from models.data.Category import Category
from sqlalchemy.orm.session import Session
from persistent.BasePersistent import BasePersistent

class CategoryPersistent(BasePersistent):
    
    def get_all_category(self):
        return self.session.query(Category).all()