from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    database_url: str
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    from_email: str
    secret_key: str = "change-me"
    term_url: str = "https://classes.usc.edu/term/20261/catalogue/program/CSCI/school/ENGV"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


try:
    settings = Settings()
except Exception as e:
    missing_vars = []
    required_vars = ["database_url", "smtp_user", "smtp_password", "from_email"]
    for var in required_vars:
        if not os.getenv(var.upper()) and not os.getenv(var):
            missing_vars.append(var.upper())
    
    if missing_vars:
        error_msg = f"""
환경 변수가 설정되지 않았습니다. Railway 대시보드에서 다음 환경 변수를 설정해주세요:

필수 환경 변수:
- DATABASE_URL (PostgreSQL 플러그인 추가 시 자동 설정)
- SMTP_USER (이메일 계정)
- SMTP_PASSWORD (이메일 앱 비밀번호)
- FROM_EMAIL (발신자 이메일 주소)

설정되지 않은 변수: {', '.join(missing_vars)}

Railway 설정 방법:
1. Railway 프로젝트 대시보드로 이동
2. Variables 탭 클릭
3. 각 환경 변수를 추가하고 저장
        """
        print(error_msg)
        raise ValueError(error_msg) from e
    raise
