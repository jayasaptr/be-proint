import os
from datetime import timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from urllib.parse import quote_plus

load_dotenv()

def sqlserver_uri() -> str:
    """Create SQL Server connection URI"""
    driver = os.getenv("DB_SQLSERVER_CONNECTION", "ODBC Driver 17 for SQL Server")
    host = os.getenv("DB_SQLSERVER_HOST", "localhost")
    port = os.getenv("DB_SQLSERVER_PORT", "1433")
    database = os.getenv("DB_SQLSERVER_DATABASE", "").strip('"')
    username = os.getenv("DB_SQLSERVER_USERNAME", "")
    password = os.getenv("DB_SQLSERVER_PASSWORD", "")

    # Using pymssql (simpler, no ODBC driver needed)
    return f"mssql+pymssql://{username}:{quote_plus(password)}@{host}:{port}/{database}"

    # Alternative: Using pyodbc (requires ODBC driver installation)
    # params = quote_plus(f"DRIVER={{{driver}}};SERVER={host},{port};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes")
    # return f"mssql+pyodbc:///?odbc_connect={params}"

class Config:
    SQLALCHEMY_DATABASE_URI = sqlserver_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database connection pool settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "pool_size": 10,
        "max_overflow": 20,
        "pool_timeout": 30,
    }

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

def db_connection():
    """Test database connection"""
    try:
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        with engine.connect() as connection:
            print("✓ Database connection successful")
            return True
    except OperationalError as e:
        print(f"✗ Database connection failed: {e}")
        return False
