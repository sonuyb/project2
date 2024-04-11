from django import template

register = template.Library()

@register.simple_tag(name='totalsum')
def totalsum(cart):
    total = 0
    for item in cart:
        total += item.quantity*item.product.price
    return total