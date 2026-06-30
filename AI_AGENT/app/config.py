import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    MODEL_NAME = "llama-3.1-8b-instant"

    DEFAULT_DAYS = 3

    MAX_ATTRACTIONS_PER_DAY = 3