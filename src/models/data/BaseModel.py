from sqlalchemy.ext.declarative import declared_attr

class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def to_dict(self):
        """Converts the model instance to a dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @staticmethod
    def filter_fields(self):
        return []