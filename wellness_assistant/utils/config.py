"""
Configuration management for the AI Wellness Assistant
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # Database Configuration
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "data/wellness.db")
    
    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Data Directory
    DATA_DIR: Path = Path("data")
    
    # Ensure data directory exists
    @classmethod
    def ensure_data_dir(cls) -> None:
        """Ensure the data directory exists"""
        cls.DATA_DIR.mkdir(exist_ok=True)
    
    # Ethical Guidelines
    MEDICAL_DISCLAIMER = (
        "⚠️  IMPORTANT DISCLAIMER: This advice is for general wellness purposes only. "
        "It is not a substitute for professional medical advice, diagnosis, or treatment. "
        "Always consult with a qualified healthcare provider for medical concerns."
    )
    
    # Red Flag Symptoms (require immediate medical attention)
    RED_FLAG_SYMPTOMS = [
        "chest pain", "chest pressure", "chest tightness",
        "shortness of breath", "difficulty breathing", "can't breathe",
        "sudden severe headache", "severe headache",
        "vision loss", "loss of vision", "sudden vision changes",
        "weakness on one side", "facial drooping", "speech problems",
        "severe abdominal pain", "severe stomach pain",
        "blood in stool", "blood in urine", "coughing blood",
        "high fever", "fever over 103", "sudden confusion",
        "severe allergic reaction", "difficulty swallowing",
        "loss of consciousness", "fainting", "seizure"
    ]
