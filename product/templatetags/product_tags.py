from django import template
from product.utils import is_liked_product

register = template.Library()


@register.simple_tag(takes_context=True)
def is_liked(context, product, success, fail):
    """
    Return string from 'success' if user likes product else return 'fail'
    string.
    """
    user = context['request'].user
    return success if is_liked_product(product, user) else fail
