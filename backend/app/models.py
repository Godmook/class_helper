from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    courses = relationship("Course", back_populates="user", cascade="all, delete-orphan")


class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_number = Column(String, nullable=False)  # e.g., "535"
    course_name = Column(String, nullable=True)
    current_registered = Column(String, nullable=True)  # e.g., "50/50"
    is_available = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="courses")
    logs = relationship("CrawlerLog", back_populates="course", cascade="all, delete-orphan")


class CrawlerLog(Base):
    __tablename__ = "crawler_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    registered_info = Column(String, nullable=True)  # e.g., "49/50"
    is_available = Column(Boolean, default=False)
    screenshot_path = Column(String, nullable=True)
    crawled_at = Column(DateTime(timezone=True), server_default=func.now())
    
    course = relationship("Course", back_populates="logs")
