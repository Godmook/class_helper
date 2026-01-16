from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Railway에서 PostgreSQL 추가 시 자동으로 설정됨
    # DATABASE_URL 또는 POSTGRES_URL 등 여러 이름 지원
    database_url: str = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or ""
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    from_email: str = ""
    secret_key: str = "change-me"
    term_url: str = "https://classes.usc.edu/term/20261/catalogue/program/CSCI/school/ENGV"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 환경 변수 없이도 서버가 시작되도록 - 검증 없이 기본값 사용
settings = Settings()

# 환경 변수 확인만 하고 경고만 출력 (에러 발생시키지 않음)
if not settings.database_url:
    print("⚠️ Warning: DATABASE_URL not set. Using SQLite as fallback.")
if not settings.smtp_user:
    print("⚠️ Warning: SMTP_USER not set. Email features will not work.")
if not settings.smtp_password:
    print("⚠️ Warning: SMTP_PASSWORD not set. Email features will not work.")
if not settings.from_email:
    print("⚠️ Warning: FROM_EMAIL not set. Email features will not work.")
