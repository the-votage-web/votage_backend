from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from uuid import UUID


class MemberDepartmentOut(BaseModel):
    id: UUID
    name: str
    directorate_id: Optional[UUID] = None
    directorate_name: Optional[str] = None
    joined_at: Optional[date] = None
    is_active: bool = True

    class Config:
        from_attributes = True


class MemberBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[str] = None
    date_of_birth: Optional[date] = None
    marital_status: Optional[str] = None
    employment_status: Optional[str] = None
    address: Optional[str] = None
    member_status: Optional[str] = "regular_member"
    date_joined: Optional[datetime] = None


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[str] = None
    date_of_birth: Optional[date] = None
    marital_status: Optional[str] = None
    employment_status: Optional[str] = None
    address: Optional[str] = None
    member_status: Optional[str] = None
    date_joined: Optional[datetime] = None


class MemberOut(MemberBase):
    id: UUID
    full_name: Optional[str] = None
    is_worker: bool = False
    departments: List[MemberDepartmentOut] = []
    department_name: Optional[str] = "Regular member"

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        deps = cls.get_departments(obj)
        is_worker = obj.is_worker or (len(deps) > 0)
        dept_name_str = ", ".join([d.name for d in deps]) if deps else "Regular member"

        return cls(
            id=obj.id,
            first_name=obj.first_name,
            last_name=obj.last_name,
            full_name=f"{obj.first_name} {obj.last_name}",
            phone_number=obj.phone_number,
            email=obj.email,
            gender=obj.gender,
            birthday=str(obj.birthday) if obj.birthday else None,
            date_of_birth=obj.date_of_birth,
            marital_status=obj.marital_status,
            employment_status=obj.employment_status,
            address=obj.address,
            member_status=obj.member_status,
            date_joined=obj.date_joined,
            is_worker=is_worker,
            departments=deps,
            department_name=dept_name_str
        )

    @staticmethod
    def get_departments(obj):
        try:
            from apps.departments.models import DepartmentMembership
            memberships = DepartmentMembership.objects.filter(
                member=obj, is_active=True
            ).select_related("department", "department__directorate")
            
            res = []
            for m in memberships:
                res.append(MemberDepartmentOut(
                    id=m.department.id,
                    name=m.department.name,
                    directorate_id=m.department.directorate.id if m.department.directorate else None,
                    directorate_name=m.department.directorate.name if m.department.directorate else None,
                    joined_at=m.joined_at,
                    is_active=m.is_active
                ))
            return res
        except Exception:
            return []


class FirstTimerBase(BaseModel):
    member_id: UUID
    service_id: Optional[UUID] = None
    service_name: str
    service_date: date
    service_type: Optional[str] = None
    heard_about_church: Optional[str] = None
    heard_about_church_other: Optional[str] = None
    purpose_of_attending: Optional[str] = None
    would_like_to_be_member: Optional[str] = None
    invited_by: Optional[str] = None
    follow_up_status: Optional[str] = "pending"
    notes: Optional[str] = None


class FirstTimerCreate(FirstTimerBase):
    pass


class FirstTimerOut(FirstTimerBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
