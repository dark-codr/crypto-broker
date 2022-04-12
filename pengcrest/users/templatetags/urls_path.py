from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def url_active(context, viewname, kwargs=None):
    request = context['request']
    current_path = request.path
    if kwargs is not None:
        compare_path = reverse(viewname, kwargs={'username':kwargs})
    else:
        compare_path = reverse(viewname)
    if current_path == compare_path:
        return 'bg-dark text-light px-3 py-2'
    else:
        return ''

@register.simple_tag(takes_context=True)
def url_target(context, viewname, kwargs=None):
    request = context['request']
    current_path = request.path
    if kwargs is not None:
        compare_path = reverse(viewname, kwargs={'username':kwargs})
    else:
        compare_path = reverse(viewname)
    if current_path != compare_path:
        return 'hover-target'
    else:
        return ''