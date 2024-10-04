from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsStaffOrReadonly(BasePermission):
    """
    Every user can make a safe request.
    Only staff can create or delete object instance.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_staff
            and request.user.is_active
        )


class IsOwnerOrIsStaffOrReadOnly(BasePermission):
    """
    Every user can make safe request.
    Only staff or owner can edit or delete object instance.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
        )

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS
                    or request.user.is_authenticated
                    and request.user.is_active
                    and (request.user == obj.owner or request.user.is_staff)
                    )
