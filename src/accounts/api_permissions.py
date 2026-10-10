"""DRF permission classes implementing object-level RBAC for Phase 3 reuse."""


class OwnerOrReadOnly:
    """
    Read for everyone; write/delete only for the object's owner.
    Staff/superusers and admin-role users may write anything.
    Expects the object to expose `owner`.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        user = request.user
        if user.is_superuser or getattr(user, "role", "") == "admin":
            return True
        return getattr(obj, "owner_id", None) == user.pk


class EditorCanDelete:
    """
    Phase 3 refinement (DoD: "başkasının dosyası silinemez"):
    delete allowed only for the owner or an admin. Editors may delete
    their own uploads (covered by owner check).
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            user = request.user
            if user.is_superuser or getattr(user, "role", "") == "admin":
                return True
            return getattr(obj, "owner_id", None) == user.pk
        return True
