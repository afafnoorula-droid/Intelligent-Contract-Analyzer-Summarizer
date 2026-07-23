import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///contracts.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "your_super_secret_key_here_for_jwt")
    
    CHROMA_PATH = "./chroma_db"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    LLM_MODEL = "llama-3.3-70b-versatile"
    
    UPLOAD_FOLDER = "uploads"
    REPORTS_FOLDER = "reports"
    
    DEBUG = True
    MAX_TEXT_LENGTH = 50000  # For handling large contracts
    SUPPORTED_LANGUAGES = ["en", "ar"]  # English + Arabic    
    