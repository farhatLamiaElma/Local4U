from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def sum_cart_total(cart_items):
    total = 0
    for item in cart_items:
        total += float(item['price']) * item['quantity']
    return total

@register.filter
def is_not_farmer_or_admin(user):
    return user.is_authenticated and user.user_type not in ['farmer', 'admin']