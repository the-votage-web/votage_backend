from typing import Optional, List
from pydantic import BaseModel
from datetime import date
from uuid import UUID


class ServiceTypeBase(BaseModel):
    name: str
    description: Optional[str] = ""
    is_recurring: bool = False


class ServiceTypeCreate(ServiceTypeBase):
    pass


class ServiceTypeOut(ServiceTypeBase):
    id: UUID

    class Config:
        from_attributes = True


class ServiceBase(BaseModel):
    name: str
    theme: Optional[str] = None
    location: Optional[str] = None
    service_type_id: Optional[UUID] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    service_type_id: Optional[UUID] = None
    theme: Optional[str] = None
    location: Optional[str] = None


class ServiceOut(ServiceBase):
    id: UUID
    service_type_name: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        if hasattr(obj, "service_type") and obj.service_type:
            data.service_type_name = obj.service_type.name
        return data
