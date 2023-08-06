from rest_framework.permissions import BasePermission


class HolgerPermission(BasePermission):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
