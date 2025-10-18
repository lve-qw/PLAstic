from django import template

register = template.Library()

@register.simple_tag
def modify_query_string(**kwargs):
    """
    Creates a query string with modified parameters
    Usage: ?{% modify_query_string page=2 sort='price_asc' %}
    """
    from django.http import QueryDict
    from django.utils.http import urlencode
    
    query_dict = QueryDict(mutable=True)
    
    # Copy existing GET parameters
    for key, value in kwargs.pop('existing_params', {}).items():
        if value:
            query_dict[key] = value
    
    # Add/update new parameters
    for key, value in kwargs.items():
        if value is not None and value != '':
            query_dict[key] = value
    
    return query_dict.urlencode()

@register.simple_tag(takes_context=True)
def modify_query(context, **kwargs):
    """
    Creates a query string with modified parameters using current request
    """
    request = context['request']
    existing_params = request.GET.copy()
    
    # Remove page parameter if we're changing pages
    if 'page' in kwargs:
        if 'page' in existing_params:
            del existing_params['page']
    
    # Update with new parameters
    for key, value in kwargs.items():
        if value is not None and value != '':
            existing_params[key] = value
        elif key in existing_params:
            del existing_params[key]
    
    return existing_params.urlencode()