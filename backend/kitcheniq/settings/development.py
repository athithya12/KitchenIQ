from .base import *

# --- 1. LOCAL OVERRIDES ---
DEBUG = env.bool('DEBUG', default=True) # Enables Django debugging mode

# --- 2. MinIO Configuration (Local S3 Emulator) ---
# These settings override the default AWS S3 behavior defined in base.py
# and point the S3 client (boto3) to the MinIO container service.
AWS_S3_ENDPOINT_URL = env.str('AWS_S3_ENDPOINT_URL', default='http://minio:9000')
AWS_S3_SECURE_URLS = False # MinIO runs over plain HTTP in dev environment
AWS_ACCESS_KEY_ID = env.str('MINIO_ACCESS_KEY', default='insecure-default-access-key') # Credentials from docker-compose
AWS_SECRET_ACCESS_KEY = env.str('MINIO_SECRET_KEY', default='insecure-default-secret-key') # Credentials from docker-compose