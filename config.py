import os
from dotenv import load_dotenv

load_dotenv()

# Crawling config
CRAWL_URL = "https://www.purtirealty.com/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
MAX_CRAWL_PAGES = 100  # Safety limit

# Clustering config
CLUSTERING_DISTANCE_THRESHOLD = 0.4
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# LLM config
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LLM_MODEL_NAME = "gemini-2.0-flash-thinking-exp-01-21"
LLM_TEMPERATURE = 1