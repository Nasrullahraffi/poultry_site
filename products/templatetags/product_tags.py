"""
Custom template tags for products app
"""
from django import template

register = template.Library()

@register.filter
def divisible(value, arg):
    """Divide the value by the argument"""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value, total):
    """Calculate percentage of value from total"""
    try:
        if total == 0:
            return 0
        return (float(value) / float(total)) * 100
    except (ValueError, ZeroDivisionError, TypeError):
        return 0

@register.filter
def stock_percentage(product):
    """Calculate stock percentage based on reorder point"""
    try:
        if not product.reorder_point or product.reorder_point == 0:
            return 100
        stock = product.stock_on_hand if product.stock_on_hand else 0
        percentage = (float(stock) / float(product.reorder_point)) * 100
        return min(percentage, 100)  # Cap at 100%
    except (ValueError, ZeroDivisionError, TypeError, AttributeError):
        return 0

@register.filter
def needs_reorder(product):
    """Check if product needs reorder"""
    try:
        if not product.reorder_point:
            return False
        stock = product.stock_on_hand if product.stock_on_hand else 0
        return stock <= product.reorder_point
    except (AttributeError, TypeError):
        return False

