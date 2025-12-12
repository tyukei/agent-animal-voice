import os
from dotenv import load_dotenv

load_dotenv()
LLM_MODEL_ID = os.getenv('LLM_MODEL_ID')
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
STAGING_BUCKET = f"gs://{PROJECT_ID}-agent-engine-bucket"