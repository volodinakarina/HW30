from functools import wraps

from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed

from users.models import UserRoles


class IsOwner(permissions.BasePermission):
    message = 'Updating/deleting not your selection is not permitted'

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            owner = obj.owner
        elif hasattr(obj, 'author'):
            owner = obj.author
        else:
            raise Exception('Something wrong with permissions...')

        return owner == request.user


class IsAdmin(permissions.BasePermission):
    message = 'Only admin/moderator has permission'

    def has_permission(self, request, view):
        return request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]