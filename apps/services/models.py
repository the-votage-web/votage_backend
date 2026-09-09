import uuid
from django.db import models
from django.utils import timezone


class ServiceType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "service_types"
        managed = True


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80, default="Sunday Service")
    theme = models.CharField(max_length=80, null=True, blank=True)
    location = models.CharField(max_length=80, null=True, blank=True)
    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.theme or 'No Theme'})"

    class Meta:
        db_table = "service"
        managed = True
