from rest_framework import permissions


class IsOvnerOnlyRead(permissions.BasePermission):
    def has_permission(self, request, view):
        """Разрешаем доступ для всех методов, кроме POST, PUT и DELETE"""
        if request.method in permissions.SAFE_METHODS:
            return True
  