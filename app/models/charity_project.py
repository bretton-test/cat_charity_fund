from sqlalchemy import Column, String, Text

from app.core.db import Base, Charity


class CharityProject(Base, Charity):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
