from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID


class ConnectGroupBase(BaseModel):
    name: str
    description: Optional[str] = ""
    meeting_day: str
    meeting_time: Optional[str] = ""
    service_id: Optional[UUID] = None


class ConnectGroupCreate(ConnectGroupBase):
    pass


class ConnectGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    meeting_day: Optional[str] = None
    meeting_time: Optional[str] = None
    service_id: Optional[UUID] = None


class ConnectGroupOut(ConnectGroupBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ConnectGroupMemberBase(BaseModel):
    connect_group_id: UUID
    member_id: UUID
    joined_at: Optional[date] = None
    left_at: Optional[date] = None


class ConnectGroupMemberCreate(ConnectGroupMemberBase):
    pass


class ConnectGroupMemberOut(ConnectGroupMemberBase):
    id: UUID
    member_name: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        if hasattr(obj, "member") and obj.member:
            data.member_name = f"{obj.member.first_name} {obj.member.last_name}"
        return data


class ConnectGroupPastorBase(BaseModel):
    connect_group_id: UUID
    pastor_id: UUID
    start_date: date
    end_date: Optional[date] = None


class ConnectGroupPastorCreate(ConnectGroupPastorBase):
    pass


class ConnectGroupPastorOut(ConnectGroupPastorBase):
    id: UUID
    pastor_name: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        if hasattr(obj, "pastor") and obj.pastor:
            data.pastor_name = f"{obj.pastor.first_name} {obj.pastor.last_name}"
        return data
