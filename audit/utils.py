from django.conf import settings
from .models import AuditLog


def create_audit_log(request, action, object_type, object_id, description="", extra_data=None):
    user = request.user if request.user.is_authenticated else None
    ip = request.META.get("REMOTE_ADDR")
    ua = request.META.get("HTTP_USER_AGENT", "")

    AuditLog.objects.create(
        user=user,
        action=action,
        object_type=object_type,
        object_id=str(object_id),
        description=description,
        ip_address=ip,
        user_agent=ua,
        extra_data=extra_data or {},
    )
