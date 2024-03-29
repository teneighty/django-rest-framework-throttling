"""
Dumbed down version of the rest_framework module
"""

from __future__ import unicode_literals
from django.conf import settings

USER_SETTINGS = getattr(settings, 'REST_FRAMEWORK_THROTTLING', None)

DEFAULTS = {
    'DEFAULT_NEW_USER_THROTTLE': True,
    'DEFAULT_NEW_USER_THROTTLE_RATE': '100/sec',
    'ENDPOINTS': {}
}

class APISettings(object):
    def __init__(self, user_settings=None, defaults=None):
        self.defaults = defaults or {}
        self.user_settings = user_settings or {}

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        setattr(self, attr, val)
        return val

api_settings = APISettings(USER_SETTINGS, DEFAULTS)
