from django import template
from django.conf import settings
from django.core.cache import cache
from urllib import urlencode
import urllib2

ANU_URL = 'http://styles.anu.edu.au/_anu/include.php?'

register = template.Library()

def get(part, siteid):
    """Retrieves the ANU `part` content for the given `siteid`"""
    request = urllib2.Request(ANU_URL + urlencode({'part': part, 'id': siteid}))
    request.add_header('Connection', 'Close')
    response = urllib2.urlopen(request)
    return response.read()

def cacheget(part, siteid):
    """Wrapper to cache get requests"""
    cachekey = "ANUTHEME:%s:%s" % (part, siteid)
    chunk = cache.get(cachekey)
    if chunk is None:
        chunk = get(part, siteid)
        cache.set(cachekey, chunk, settings.ANU['ANUCacheTime'])
    return chunk

@register.simple_tag(takes_context=True)
def anu_banner(context):
    """Loads the ANU Banner"""
    return cacheget('banner', context['ANU']['ANUSiteID'])


@register.simple_tag(takes_context=True)
def anu_meta(context):
    """Loads the ANU Meta Content"""
    return cacheget('meta', context['ANU']['ANUSiteID'])


@register.simple_tag(takes_context=True)
def anu_footer(context):
    """Loads the ANU Footer"""
    return cacheget('footer', context['ANU']['ANUSiteID'])

    

