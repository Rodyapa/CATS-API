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
