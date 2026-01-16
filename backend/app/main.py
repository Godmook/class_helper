from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from app.database import get_db, Base, engine
from app.models import User, Course, CrawlerLog
from app.scheduler import CrawlerScheduler
from contextlib import asynccontextmanager
import os

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 전역 스케줄러
scheduler: Optional[CrawlerScheduler] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시
    global scheduler
    scheduler = CrawlerScheduler()
    await scheduler.init_crawler()
    scheduler.start()
    yield
    # 종료 시
    await scheduler.cleanup()


app = FastAPI(title="USC 수업 크롤러 API", lifespan=lifespan)

# CORS 설정 - 프론트엔드와 통신을 위해
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic 모델
class CourseCreate(BaseModel):
    course_number: str
    email: EmailStr


class CourseResponse(BaseModel):
    id: int
    course_number: str
    course_name: Optional[str]
    current_registered: Optional[str]
    is_available: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class LogResponse(BaseModel):
    id: int
    registered_info: Optional[str]
    is_available: bool
    crawled_at: datetime
    
    class Config:
        from_attributes = True


# API 엔드포인트
@app.get("/")
async def root():
    """API 루트"""
    return {"message": "USC 수업 크롤러 API", "status": "running"}


@app.get("/api/health")
async def health():
    """헬스 체크"""
    return {"status": "healthy"}


@app.post("/api/courses")
async def create_course(course_data: CourseCreate, db: Session = Depends(get_db)):
    """수업 등록"""
    # 사용자 찾기 또는 생성
    user = db.query(User).filter(User.email == course_data.email).first()
    if not user:
        user = User(email=course_data.email)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # 이미 등록된 수업인지 확인
    existing = db.query(Course).filter(
        Course.user_id == user.id,
        Course.course_number == course_data.course_number
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="이미 등록된 수업입니다.")
    
    # 수업 생성
    course = Course(
        user_id=user.id,
        course_number=course_data.course_number
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    
    return {"message": "수업이 등록되었습니다.", "course": CourseResponse.model_validate(course)}


@app.get("/api/courses", response_model=List[CourseResponse])
async def get_courses(email: str, db: Session = Depends(get_db)):
    """특정 이메일의 수업 목록 조회"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return []
    
    courses = db.query(Course).filter(Course.user_id == user.id).all()
    return [CourseResponse.model_validate(course) for course in courses]


@app.delete("/api/courses/{course_id}")
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    """수업 삭제"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="수업을 찾을 수 없습니다.")
    
    db.delete(course)
    db.commit()
    return {"message": "수업이 삭제되었습니다."}


@app.get("/api/courses/{course_id}/logs", response_model=List[LogResponse])
async def get_course_logs(course_id: int, db: Session = Depends(get_db)):
    """수업의 크롤링 이력 조회"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="수업을 찾을 수 없습니다.")
    
    logs = db.query(CrawlerLog).filter(
        CrawlerLog.course_id == course_id
    ).order_by(CrawlerLog.crawled_at.desc()).limit(50).all()
    
    return [LogResponse.model_validate(log) for log in logs]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
