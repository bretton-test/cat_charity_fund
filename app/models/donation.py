from sqlalchemy import Column, Text, Integer, ForeignKey

from app.core.db import Base, Charity


class Donation(Base, Charity):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
