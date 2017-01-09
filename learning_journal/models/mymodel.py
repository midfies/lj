from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Date,
)

from .meta import Base


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    body = Column(Unicode)
    category = Column(Unicode)
    tags = Column(Unicode)
    creation_date = Column(Date)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'category': self.category,
            'tags': self.tags,
            'creation_date': self.creation_date
        }
