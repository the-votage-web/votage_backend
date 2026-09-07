from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class EventBase(BaseModel):
    service_id: UUID
    event_type: str
    description: Optional[str] = ""


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    service_id: Optional[UUID] = None
    event_type: Optional[str] = None
    description: Optional[str] = None


class EventOut(EventBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class EventParticipationBase(BaseModel):
    event_id: UUID
    member_id: Optional[UUID] = None
    participant_name: str
    role: str


class EventParticipationCreate(EventParticipationBase):
    pass


class EventParticipationOut(EventParticipationBase):
    id: UUID

    class Config:
        from_attributes = True
