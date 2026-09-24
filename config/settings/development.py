from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True
# emails print to terminal, nothing sends
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# all endpoints open while building — tighten per-view with permission_classes
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}
