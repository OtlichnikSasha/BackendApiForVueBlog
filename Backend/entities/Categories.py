from app_config import db
from sqlalchemy import Column, Integer, String, ForeignKey

class Categories(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(255), nullable=False)
    text = Column(String(10000), nullable=False)
    views = 0

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


    def __repr__(self):
        return f'<categories {self.id}>'

