import uuid
from django.db import models
from django.utils import timezone
from djangoyearlessdate.models import YearlessDateField


class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    gender = models.CharField(max_length=32, null=True, blank=True)
    birthday = YearlessDateField(max_length=4, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=32, null=True, blank=True)
    employment_status = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    is_worker = models.BooleanField(default=False)
    member_status = models.CharField(max_length=32, default="regular_member")
    date_joined = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'members'
        managed = True


class FirstTimers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="first_timer_records")
    service = models.ForeignKey("services.Service", null=True, blank=True, on_delete=models.SET_NULL, related_name="first_timers")
    service_name = models.CharField(max_length=200, default="Sunday Service")
    service_date = models.DateField(default=timezone.now)
    service_type = models.CharField(max_length=50, blank=True, null=True)
    heard_about_church = models.CharField(max_length=50, blank=True, null=True)
    heard_about_church_other = models.CharField(max_length=200, blank=True, null=True)
    purpose_of_attending = models.TextField(blank=True, null=True)
    would_like_to_be_member = models.CharField(max_length=20, blank=True, null=True)
    invited_by = models.CharField(max_length=150, blank=True, null=True, help_text="Person who invited the first timer")
    follow_up_status = models.CharField(max_length=50, default="pending")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FirstTimer: {self.member} - {self.service_date}"

    class Meta:
        db_table = 'first_timer_events'
        managed = True
