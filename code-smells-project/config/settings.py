import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "minha-chave-super-secreta-123")
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    DB_PATH = os.getenv("DB_PATH", "loja.db")
