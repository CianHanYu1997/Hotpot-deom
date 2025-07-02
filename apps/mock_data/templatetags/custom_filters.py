from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    return dictionary.get(key, 0)


@register.filter
def sub(value, arg):
    """Subtract the arg from the value"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        try:
            return float(value) - float(arg)
        except (ValueError, TypeError):
            return 0


@register.filter
def div(value, arg):
    """Divide the value by the arg"""
    try:
        return int(value) / int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        try:
            return float(value) / float(arg)
        except (ValueError, TypeError, ZeroDivisionError):
            return 0


@register.filter
def mul(value, arg):
    """Multiply the value by the arg"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        try:
            return float(value) * float(arg)
        except (ValueError, TypeError):
            return 0


@register.filter
def abs_value(value):
    """Return the absolute value"""
    try:
        return abs(int(value))
    except (ValueError, TypeError):
        try:
            return abs(float(value))
        except (ValueError, TypeError):
            return 0
