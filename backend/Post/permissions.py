from rest_framework import permissions

class IsOwnerOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view, obj):
        return obj.posted_by == request.user