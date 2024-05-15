from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Разрешение только на автора или администратора."""

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and obj.user == request.user
            or request.user.is_staff
        )
