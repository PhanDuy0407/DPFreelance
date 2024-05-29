from models.data.Category import Category
from sqlalchemy.orm.session import Session

class CategoryPersistent:
    def __init__(self, session):
        self.session: Session = session
    
    def get_all_category(self):
        return self.session.query(Category).all()