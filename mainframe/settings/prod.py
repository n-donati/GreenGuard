import io
import os
from urllib.parse import urlparse
from pathlib import Path
import environ
from django.core.exceptions import ImproperlyConfigured
# Import the original settings from each template
from .basesettings import *
import json
from google.oauth2 import service_account

# Load the settings from the environment variable
env = environ.Env()
env.read_env(io.StringIO(os.environ.get("APPLICATION_SETTINGS", None)))
PROD = True if env('DJANGO_SETTINGS_MODULE') == 'mainframe.settings.prod' else False
# Setting this value from django-environ
SECRET_KEY = env("SECRET_KEY")

if "mainframe" not in INSTALLED_APPS:
  INSTALLED_APPS.append("mainframe")
if "storages" not in INSTALLED_APPS:
  INSTALLED_APPS.append("storages")
# If defined, add service URL to Django security settings
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
  ALLOWED_HOSTS = [
      urlparse(CLOUDRUN_SERVICE_URL).netloc,
  ]
  CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL, ]
else:
  ALLOWED_HOSTS = ["*"]

# Default false. True allows default landing pages to be visible
DEBUG = env("DEBUG", default=False)

# Set this value from django-environ
DATABASES = {"default": env.db()}

if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
  DATABASES["default"]["HOST"] = "127.0.0.1"
  DATABASES["default"]["PORT"] = 5432
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
STATICFILES_DIRS = [BASE_DIR / 'static']
secret_json = env("SERVICE_ACCOUNT_CREDENTIALS")
creds_dict = json.loads(secret_json)
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(creds_dict)
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
DEFAULT_FILE_STORAGE = 'mainframe.cloudstorage.CustomGoogleCloudStorage'