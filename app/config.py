import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret')
    raw_password = os.getenv('DB_PASSWORD', '')
    safe_password = quote_plus(raw_password)
    
    #Configuracion de la DB
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{safe_password}"  # <-- AQUÍ cambiamos a safe_password
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
