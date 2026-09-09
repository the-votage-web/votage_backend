import uuid
from django.db import models
from django.utils import timezone


class Directorate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    director = models.ForeignKey(
        "members.Member",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="directorates_led"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "directorate"
        managed = True


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    directorate = models.ForeignKey(
        Directorate,
        on_delete=models.CASCADE,
        related_name="departments",
        null=True,
        blank=True
    )
    hod = models.ForeignKey(
        "members.Member",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="departments_led"
    )
    assistant_hod = models.ForeignKey(
        "members.Member",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="departments_assisted"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "department"
        managed = True


class DepartmentMembership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(
        "members.Member",
        on_delete=models.CASCADE,
        related_name="department_memberships"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    joined_at = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "department_memberships"
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=["member", "department"],
                name="unique_member_department"
            )
        ]
        indexes = [
            models.Index(fields=["member"]),
            models.Index(fields=["department"]),
        ]

    def __str__(self):
        return f"{self.member} - {self.department}"


class Unit(models.Model):
    """
    Sub-division / Unit inside a Department.
    Example: Media department -> Live Streaming, Camera, Graphics, etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="units"
    )
    unit_head = models.ForeignKey(
        "members.Member",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="units_led",
        verbose_name="Unit Head / Assistant HOD"
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "units"
        managed = True
        unique_together = [("name", "department")]
        ordering = ["name"]
        indexes = [
            models.Index(fields=["department"]),
            models.Index(fields=["unit_head"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.department.name})"


class UnitMembership(models.Model):
    """
    Many-to-many link between Member <-> Unit
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(
        "members.Member",
        on_delete=models.CASCADE,
        related_name="unit_memberships"
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    joined_at = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    role = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. Camera Operator, Graphics Designer, Stream Technician..."
    )

    class Meta:
        db_table = "unit_memberships"
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=["member", "unit"],
                name="unique_member_unit"
            )
        ]
        indexes = [
            models.Index(fields=["member"]),
            models.Index(fields=["unit"]),
        ]

    def __str__(self):
        return f"{self.member} — {self.unit}"
