from django import template

register = template.Library()


@register.filter
def mediapath(image):
    from django.conf import settings
    media_url = settings.MEDIA_URL
    return media_url + image
