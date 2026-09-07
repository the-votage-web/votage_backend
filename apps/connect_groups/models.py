import uuid
from django.db import models
from django.utils import timezone


class ConnectGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(
        "services.Service",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="connect_groups"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    meeting_day = models.CharField(max_length=20)
    meeting_time = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "connect_group"
        managed = True


class ConnectGroupMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    connect_group = models.ForeignKey(
        ConnectGroup,
        on_delete=models.CASCADE,
        related_name="members"
    )
    member = models.ForeignKey(
        "members.Member",
        on_delete=models.CASCADE,
        related_name="connect_group_memberships"
    )
    joined_at = models.DateField(default=timezone.now)
    left_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member} in {self.connect_group}"

    class Meta:
        db_table = "connect_group_members"
        managed = True


class ConnectGroupPastor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    connect_group = models.ForeignKey(
        ConnectGroup,
        on_delete=models.CASCADE,
        related_name="pastor_assignments"
    )
    pastor = models.ForeignKey(
        "pastors.Pastor",
        on_delete=models.CASCADE,
        related_name="connect_groups"
    )
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.pastor} - {self.connect_group}"

    class Meta:
        db_table = "connect_group_pastors"
        managed = True