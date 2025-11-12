"""
Navigation template tags for active link highlighting.
"""
from django import template
from django.urls import resolve, Resolver404

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, url_name, **kwargs):
    """
    Returns 'active' if the current request matches the given URL name.

    Usage:
        {% load nav %}
        <li class="{% active 'home' %}">

    Args:
        context: Template context (contains request)
        url_name: The name of the URL pattern to check
        **kwargs: Optional URL parameters

    Returns:
        str: 'active' if current URL matches, empty string otherwise
    """
    request = context.get('request')
    if not request:
        return ''

    try:
        # Get current URL name
        current_url = resolve(request.path_info)

        # Check if URL names match
        if current_url.url_name == url_name:
            return 'active'

        # Also check namespace + url_name (e.g., 'starships:ship_list')
        if ':' in url_name:
            full_name = f"{current_url.namespace}:{current_url.url_name}" if current_url.namespace else current_url.url_name
            if full_name == url_name:
                return 'active'
    except (Resolver404, AttributeError):
        pass

    return ''


@register.simple_tag(takes_context=True)
def active_parent(context, *url_names):
    """
    Returns 'active' if the current request matches any of the given URL names.
    Useful for parent menu items with multiple child pages.

    Usage:
        {% load nav %}
        <li class="{% active_parent 'starships:ship_list' 'starships:ship_detail' %}">

    Args:
        context: Template context (contains request)
        *url_names: Variable number of URL pattern names to check

    Returns:
        str: 'active' if any URL matches, empty string otherwise
    """
    request = context.get('request')
    if not request:
        return ''

    try:
        current_url = resolve(request.path_info)
        current_full_name = f"{current_url.namespace}:{current_url.url_name}" if current_url.namespace else current_url.url_name

        for url_name in url_names:
            if current_url.url_name == url_name or current_full_name == url_name:
                return 'active'
    except (Resolver404, AttributeError):
        pass

    return ''
