from django.http import HttpResponseBadRequest
from django.utils.timezone import localtime
from product.models import Like


def is_liked_product(product, user):
    """
    :return True if user already like current product
    """
    return user.is_authenticated() and Like.objects.filter(
            user=user, product=product).exists()


def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """
    def wrap(request, *args, **kwargs):
            if not request.is_ajax():
                return HttpResponseBadRequest()
            return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def make_localtime(datetime_obj):
    """
    convert UTC time to time in current timezone
    """
    return localtime(datetime_obj).strftime("%Y-%m-%d %H:%M:%S")
