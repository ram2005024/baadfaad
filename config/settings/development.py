from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True
# emails print to terminal, nothing sends
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# all endpoints open while building — tighten per-view with permission_classes
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}
# File storage for s3
DEFAULT_FILE_STORAGES="storages.backends.s3boto3.S3Boto3Storage"
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="ap-south-1")
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/"