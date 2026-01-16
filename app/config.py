from pydantic_settings import BaseSettings
from typing import Optional


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
        case_sensitive = False


settings = Settings()
