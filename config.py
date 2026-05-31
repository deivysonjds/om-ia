"""
Configurações da aplicação.
"""

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
URL_API = os.getenv("URL_API", "")

LLM_MODEL = "gpt-4.1-mini"