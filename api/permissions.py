from rest_framework import permissions


class IsOvnerReadChange(permissions.BasePermission):
    """Разрешение на получение списка задач и изменения статуса задачи"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Разрешаем доступ для всех методов, кроме POST, PUT и DELETE
            return True
        return obj.user == request.user  # Разрешает для всех остольных методов
