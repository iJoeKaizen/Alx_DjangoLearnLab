from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow read access to anyone, write/delete only to owner.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS allowed for all
        if request.method in permissions.SAFE_METHODS:
            return True
        # assume model has `author` ForeignKey
        return getattr(obj, "author", None) == request.user
