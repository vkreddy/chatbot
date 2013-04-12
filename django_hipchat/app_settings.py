from django.conf import settings

def setting(suffix, default):
    return getattr(settings, 'HIPCHAT_%s' % suffix, default)

ENABLED = setting('ENABLED', True)
BACKEND = setting('BACKEND', 'django_hipchat.backends.urllib_backend')
AUTH_TOKEN = setting('AUTH_TOKEN', None)
MESSAGE_FROM = setting('MESSAGE_FROM', None)
MESSAGE_ROOM = setting('MESSAGE_ROOM', None)
FAIL_SILENTLY = setting('FAIL_SILENTLY', False)
