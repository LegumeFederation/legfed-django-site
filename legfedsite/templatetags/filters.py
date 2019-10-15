from django import template

register = template.Library()

# Filter for dictionary lookup, used like {{ d|dictget:"key" }} in template
@register.filter
def dictget(d, key):
    return d.get(key)

# Remove a filter tag from the string
@register.filter
def cuttag(s, key) :
    i0 = s.find('&%s='%(key))
    if i0 < 0 :
        return s
    i1 = s.find('&', i0 + 1)
    if i1 < 0 :
        tag = s[i0:]
    else :
        tag = s[i0:i1]
    return s.replace(tag, '')

# Convert ch to space
@register.filter
def spacify(s, ch) :
    return s.replace(ch, ' ')

