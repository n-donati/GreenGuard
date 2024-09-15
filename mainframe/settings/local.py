import io
import os
from urllib.parse import urlparse
from .basesettings import *
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG')
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

PROD = True if os.getenv('DJANGO_SETTINGS_MODULE') == 'mainframe.settings.prod' else False
# If you have global static files, not tied to any particular app
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # This line is needed to define the location
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default file storage
DEFAULT_FILE_STORAGE = 'mainframe.cloudstorage.CustomGoogleCloudStorage'