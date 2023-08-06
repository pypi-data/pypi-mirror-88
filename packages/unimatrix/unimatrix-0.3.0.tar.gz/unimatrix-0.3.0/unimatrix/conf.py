"""Exposes the settings declared in the environment variable
``UNIMATRIX_SETTINGS_MODULE``."""
import importlib
import os

import unimatrix.environ
from unimatrix.exceptions import ImproperlyConfigured


class Settings:
    """Proxy object to load settings lazily."""
    not_initialized = object()

    def __init__(self):
        self.module = self.not_initialized

    def _get_settings_module(self):
        os.environ.setdefault('DEPLOYMENT_ENV', 'production')
        settings = None
        if os.getenv('UNIMATRIX_SETTINGS_MODULE'):
            module_qualname = os.getenv('UNIMATRIX_SETTINGS_MODULE')
            try:
                settings = importlib.import_module(module_qualname)
            except ImportError:
                raise ImproperlyConfigured(
                    "Can not import settings module %s" % module_qualname)
        return settings

    def __getattr__(self, attname):
        if self.module == self.not_initialized:
            self.module = self._get_settings_module()
        value = getattr(self.module, attname, self.not_initialized)
        if value == self.not_initialized:
            value = getattr(unimatrix.environ, attname)
        return value


settings = Settings()
