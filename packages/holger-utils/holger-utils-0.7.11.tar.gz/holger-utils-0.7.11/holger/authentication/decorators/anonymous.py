from django.core.exceptions import PermissionDenied


def anonymous_required(function=None, redirect_url=None):
    """
    The way to use this decorator is:
        @anonymous_required
        def my_view(request, pk)
        ...
    """

    def wrap(request, *args, **kwargs):
        if not request.user.is_anonymous():
            raise PermissionDenied
        return function(request, *args, **kwargs)

    return wrap
