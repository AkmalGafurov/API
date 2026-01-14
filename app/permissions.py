from rest_framework.permissions import BasePermission
from django.utils import timezone
from datetime import timedelta


class CanUpdate4Hours(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH']:
            time_limit = obj.created_at + timedelta(hours=4)
            return timezone.now() <= time_limit

        return True