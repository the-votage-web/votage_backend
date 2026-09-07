import uuid
from django.db import models


class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(
        "members.Member",
        on_delete=models.CASCADE,
        related_name="attendances"
    )
    service = models.ForeignKey(
        "services.Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attendances"
    )
    service_type = models.CharField(max_length=32)
    connect_name = models.CharField(max_length=80, null=True, blank=True)
    checkin_code = models.CharField(max_length=32, unique=True, null=True, blank=True)
    service_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "attendance"
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=["member", "service_date", "service_type", "connect_name"],
                name="uq_member_day_service_connect"
            )
        ]

    def __str__(self):
        return f"{self.member} - {self.service_date} ({self.service_type})"
