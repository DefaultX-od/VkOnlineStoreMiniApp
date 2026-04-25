from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship

from .base import Base

class DropPoint(Base):
    __tablename__ = 'drop_points'

    id = Column(Integer, name='drop_point_id', primary_key=True)
    country = Column(String, name='country')
    city = Column(String, name='city')
    street = Column(String, name='street')
    building = Column(String, name='building')
    note = Column(String, name='notes')
    is_hidden = Column(Boolean, name='is_hidden')

    def to_dic(self):
        return {
            'id' : self.id,
            'text' : ', '.join([str(self.country), str(self.city), str(self.street), str(self.building)]),
            'note' : self.note
        }
