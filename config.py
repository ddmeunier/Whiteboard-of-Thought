from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    OPENAI_API = os.getenv("OPENAI_API")
    CURRENT_MODEL = os.getenv("CURRENT_MODEL")

