from django import template

register = template.Library()

@register.filter
def in_category(things, category):
    return things.filter(category=category)

@register.filter
def get_username(links, cat):
    for link in links:
        if link.category == cat:
            return link.account.username