# Settings package: manage.py keeps using DJANGO_SETTINGS_MODULE=config.settings,
# which re-exports base settings. Select test/prod explicitly when needed.
from config.settings.base import *  # noqa: F401,F403
