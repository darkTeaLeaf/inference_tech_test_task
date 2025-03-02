from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow senders of an message to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow users themselves to edit their user information.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
