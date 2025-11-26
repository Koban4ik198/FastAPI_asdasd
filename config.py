from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings

class DBSettings(BaseSettings):
    DB_URL: str = "sqlite:///./test.db"
    
    def get_engine(self):
        return create_engine(self.DB_URL)
    
    def get_session(self):
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        return Session()

# Создаем экземпляр настроек
db_settings = DBSettings()