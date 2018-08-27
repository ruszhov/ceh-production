# from django import template
# register = template.Library()

# @register.simple_tag
# def url_replace(request, field, value):
#     d = request.GET.copy()
#     d[field] = value
#     return d.urlencode()

# @register.simple_tag
# def url_delete(request, field):
#     d = request.GET.copy()
#     del d[field]
#     return d.urlencode()

from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_param(context):
    get_param = []
    request = context['request']
    for key, v in request.GET.items():
        value_list = request.GET.getlist(key)
        get_param.extend(['%s=%s' % (key, val) for val in value_list if key != 'page'])
    return '&'.join(get_param)
    # print('&'.join(get_param))