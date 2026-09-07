import uuid
from django.db import models


class GrowthTrack(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cohort_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cohort_name} ({self.status})"

    class Meta:
        db_table = "growth_tracks"
        managed = True


class GrowthTrackEnrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    growth_track = models.ForeignKey(
        GrowthTrack,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    member = models.ForeignKey(
        "members.Member",
        on_delete=models.CASCADE,
        related_name="growth_track_enrollments"
    )
    enrollment_date = models.DateField()

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("dropped", "Dropped"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    graduation_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "growth_track_enrollments"
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=["growth_track", "member"],
                name="unique_growth_track_enrollment"
            )
        ]

    def __str__(self):
        return f"{self.member} in {self.growth_track}"
