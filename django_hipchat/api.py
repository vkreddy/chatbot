import urllib
import urllib2

from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string

from . import app_settings

def hipchat_message(template, context=None, fail_silently=app_settings.FAIL_SILENTLY):
    """

     * Add ``django_hipchat`` to ``INSTALLED_APPS``

     * Ensure ``django.template.loaders.app_directories.Loader`` is in your
       ``TEMPLATE_LOADERS``.

    >>> from django_hipchat.api import message
    >>> message("path/to/my_message.hipchat", {
        'foo': Foo.objects.get(pk=17),
    })

    path/to/my_message.hipchat::

        {% extends django_hipchat %}

        {% block room_id %}
        Room to spam
        {% endblock %}

        {% block message %}
        Message text here: {{ foo.bar|urlize }}
        {% endblock %}

        {% block color %}
        red
        {% endblock %}

    Required blocks:

     * message

    Required blocks which can be defaulted globally and overriden:

     * auth_token
     * room_id
     * from

    Optional blocks:

     * color
    """

    if not app_settings.ENABLED:
        return

    context = Context(context or {})

    context['settings'] = settings

    def render(component):
        component_template = 'django_hipchat/%s' % component

        return render_to_string(template, {
            'django_hipchat': component_template,
        }, context).strip().encode('utf8', 'ignore')

    data = {
        'from': app_settings.MESSAGE_FROM,
        'color': 'yellow',
        'message': '',
        'room_id': app_settings.MESSAGE_ROOM,
        'auth_token': app_settings.AUTH_TOKEN,
        'message_format': 'html',
    }

    for part in ('auth_token', 'room_id', 'message', 'color', 'from'):
        try:
            txt = render(part)
        except Exception:
            if fail_silently:
                return
            raise

        if txt:
            data[part] = txt

    for x in ('auth_token', 'from', 'message', 'room_id'):
        if data[x]:
            continue

        if fail_silently:
            return

        assert False, "Missing or empty required parameter: %s" % x

    request = urllib2.Request('%s?%s' % (
        'https://api.hipchat.com/v1/rooms/message',
        urllib.urlencode(data),
    ))

    try:
        urllib2.urlopen(request)
    except Exception:
        if not fail_silently:
            raise
