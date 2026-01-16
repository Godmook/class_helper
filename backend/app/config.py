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


# 설정 검증
def validate_settings():
    missing_vars = []
    
    # DATABASE_URL 확인 (Railway PostgreSQL 자동 설정)
    db_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or os.getenv("PGDATABASE")
    if not db_url:
        missing_vars.append("DATABASE_URL (PostgreSQL 플러그인 추가 필요)")
    
    if not os.getenv("SMTP_USER"):
        missing_vars.append("SMTP_USER")
    
    if not os.getenv("SMTP_PASSWORD"):
        missing_vars.append("SMTP_PASSWORD")
    
    if not os.getenv("FROM_EMAIL"):
        missing_vars.append("FROM_EMAIL")
    
    if missing_vars:
        error_msg = f"""
환경 변수가 설정되지 않았습니다.

필수 환경 변수:
{chr(10).join('- ' + var for var in missing_vars)}

Railway 설정 방법:
1. Railway 프로젝트 → "+ New" → "Add PostgreSQL" (DATABASE_URL 자동 설정)
2. Railway 프로젝트 → "Variables" 탭에서 다음 변수 추가:
   - SMTP_USER: your_email@gmail.com
   - SMTP_PASSWORD: your_app_password
   - FROM_EMAIL: your_email@gmail.com

설정되지 않은 변수: {', '.join(missing_vars)}
        """
        print(error_msg)
        raise ValueError(error_msg)
    
    return True

try:
    validate_settings()
    settings = Settings()
except Exception as e:
    raise
