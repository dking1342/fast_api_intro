from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Blog(Base):
    __tablename__ = "blogs"
    blog_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
