from app_config import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Articles(db.Model):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(255), nullable=False)
    views = Column(Integer, default=0)
    text = Column(String(10000), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    main_img = Column(String(1024), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))

    category = relationship("Categories", backref="articles")
    author = relationship("Authors", backref="articles")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'<articles {self.id}>'

