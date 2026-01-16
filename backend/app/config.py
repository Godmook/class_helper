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

# 설정을 나중에 검증하도록 변경 (서버 시작은 허용)
def get_settings():
    """설정을 가져오되, 검증은 나중에"""
    return Settings()

# 즉시 검증하지 않고, 필요한 시점에 검증
settings = None

def init_settings():
    """설정 초기화 (필요한 시점에 호출)"""
    global settings
    if settings is None:
        try:
            settings = Settings()
            validate_settings()
        except Exception as e:
            print(f"⚠️ 환경 변수 경고: {e}")
            # 개발 환경에서는 계속 진행, 프로덕션에서는 실패
            if os.getenv("ENVIRONMENT") == "production":
                raise
            # 기본값으로 진행
            settings = Settings()
    return settings

# 처음에는 기본 설정으로 시작
try:
    settings = Settings()
    validate_settings()
except Exception as e:
    print(f"⚠️ 환경 변수 검증 실패: {e}")
    print("⚠️ 일부 기능이 작동하지 않을 수 있습니다.")
    # 기본 설정으로 진행 (에러 발생 시 재시도 가능하도록)
    settings = Settings()
