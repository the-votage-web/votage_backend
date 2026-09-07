from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID


class AttendanceBase(BaseModel):
    member_id: UUID
    service_id: Optional[UUID] = None
    service_type: str
    service_date: date
    connect_name: Optional[str] = None
    checkin_code: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceOut(AttendanceBase):
    id: UUID
    created_at: datetime
    member_name: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        if hasattr(obj, "member") and obj.member:
            data.member_name = f"{obj.member.first_name} {obj.member.last_name}"
        return data
