from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOWED_ORIGINS = ["*"]
# emails print to terminal, nothing sends
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# all endpoints open while building — tighten per-view with permission_classes
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}
