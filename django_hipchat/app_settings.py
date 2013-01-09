from django.conf import settings

def setting(suffix, default):
    return getattr(settings, 'HIPCHAT_%s' % suffix, default)

ENABLED = setting('ENABLED', True)
AUTH_TOKEN = setting('AUTH_TOKEN', None)
MESSAGE_FROM = setting('MESSAGE_FROM', None)
MESSAGE_ROOM = setting('MESSAGE_ROOM', None)
FAIL_SILENTLY = setting('FAIL_SILENTLY', False)
