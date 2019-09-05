from django import template

register = template.Library()

# Filter for dictionary lookup, used like {{ d|dictget:"key" }} in template
@register.filter
def dictget(d, key):
    return d.get(key)

