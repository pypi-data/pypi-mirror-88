"""Exposes the settings declared in the environment variable
``UNIMATRIX_SETTINGS_MODULE``."""
import importlib
import os
import sys

from unimatrix.exceptions import ImproperlyConfigured


class Settings:
    """Proxy object to load settings lazily."""
    not_initialized = object()

    def __init__(self):
        self.module = self.not_initialized

    def _get_settings_module(self):
        os.environ.setdefault('DEPLOYMENT_ENV', 'production')
        if not os.getenv('UNIMATRIX_SETTINGS_MODULE'):
            raise ImproperlyConfigured("UNIMATRIX_SETTINGS_MODULE is not defined.")
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
        return getattr(self.module, attname)


settings = Settings()
