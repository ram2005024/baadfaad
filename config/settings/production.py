from .base import *

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")


MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env(
    "AWS_S3_REGION_NAME",
    default="ap-south-1",
)
AWS_QUERYSTRING_AUTH = False
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
}

MEDIA_URL = (
    f"https://{AWS_STORAGE_BUCKET_NAME}.s3."
    f"{AWS_S3_REGION_NAME}.amazonaws.com/"
)