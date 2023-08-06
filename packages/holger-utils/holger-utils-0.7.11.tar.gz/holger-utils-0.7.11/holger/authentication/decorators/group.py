from django.contrib.auth import PermissionDenied


def group_required(function, *group_names, redirect_url=None):
    """
    Requires user membership in at least one of the groups passed in.
    The way to use this decorator is:
        @group_required(‘admins’, ‘seller’)
        def my_view(request, pk)
        ...
    """
    """
    To support modern django rest framework APIViews (class-based views).
    @method_decorator(group_required('groupa', 'groupb'))
    """

    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.is_superuser or user.groups.filter(name__in=group_names).exists():
                return function(request, *args, **kwargs)
        raise PermissionDenied

    return wrap
