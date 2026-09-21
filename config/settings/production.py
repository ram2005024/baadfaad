from .base import *

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# ── Security ─────────────────────────────────────────────────────────
# Temporary: HTTPS is not configured yet.
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Enable these after HTTPS is configured.
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# ── CORS ─────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")

# ── Static via WhiteNoise ────────────────────────────────────────────
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
