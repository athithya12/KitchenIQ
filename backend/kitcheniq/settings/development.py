# File: backend/kitcheniq/settings/development.py

import os
from pathlib import Path
import environ

# Define env object and BASE_DIR before importing base.py
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env.development')) 

# Now import the base settings, which will successfully read the variables we just loaded
from .base import *
DEBUG = env.bool('DEBUG', default=True) # Overrides the False in base.py

# --- MinIO/R2 Configuration ---
AWS_S3_ENDPOINT_URL = env.str('AWS_S3_ENDPOINT_URL')
AWS_S3_SECURE_URLS = True # Use HTTPS for cloud services
AWS_ACCESS_KEY_ID = env.str('AWS_S3_ACCESS_KEY_ID') 
AWS_SECRET_ACCESS_KEY = env.str('AWS_S3_SECRET_ACCESS_KEY')