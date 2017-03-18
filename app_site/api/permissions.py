from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsObjectOwner(BasePermission):
    message = 'You must be the owner of the post'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
