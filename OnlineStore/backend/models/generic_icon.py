from sqlalchemy import Column, Integer, String

from .base import Base

class GenericIcon(Base):
    __tablename__ = 'generic_icons'

    id = Column(Integer, name='icon_id', primary_key=True)
    name = Column(String, name='name')
    link = Column(String, name='link')