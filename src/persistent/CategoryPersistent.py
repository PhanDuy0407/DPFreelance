from models.data.Category import Category
from sqlalchemy.orm.session import Session
from persistent.BasePersistent import BasePersistent

class CategoryPersistent(BasePersistent):
    
    def get_all_category(self):
        return self.session.query(Category).all()
    
    def get_category_by_id(self, id):
        return self.session.query(Category).filter(Category.id == id).first()