import os
from pathlib import Path
from dotenv import load_dotenv

# .envファイルのパスを明示的に指定
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)
LLM_MODEL_ID = os.getenv('LLM_MODEL_ID')
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
STAGING_BUCKET = f"gs://{PROJECT_ID}-agent-engine-bucket"