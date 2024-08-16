from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

#Configs gerais da aplicação

class Settings(BaseSettings):

    API_V1_SRT: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:vistatech3011@localhost:5432/vista-tech-bd'
    DBBaseModel = declarative_base()

class Config:
    case_sensitive = True

settings = Settings()