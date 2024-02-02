from rest_framework import permissions
from .models import User


class JobOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, job):
        return request.user and request.user == job.poster


class IsShipper(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        else:
            return request.user.role == User.Roles.SHIPPER

