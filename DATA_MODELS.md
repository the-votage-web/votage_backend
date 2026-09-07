# Django Data Models Summary & Relationships

This document contains the complete normalized data model schema, entity relationship diagrams (ERD), and field specifications for all applications in this project, fully aligned with the database and Prisma schema.

## Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    Member {
        UUID id PK
        CharField first_name
        CharField last_name
        CharField phone_number
        EmailField email
        CharField gender
        CharField birthday
        DateField date_of_birth
        CharField marital_status
        CharField employment_status
        CharField address
        BooleanField is_worker
        CharField member_status
        DateTimeField date_joined
        DateTimeField created_at
        DateTimeField updated_at
    }

    FirstTimers {
        UUID id PK
        UUID member_id FK
        UUID service_id FK
        CharField service_name
        DateField service_date
        CharField service_type
        CharField heard_about_church
        CharField heard_about_church_other
        TextField purpose_of_attending
        CharField would_like_to_be_member
        CharField invited_by
        CharField follow_up_status
        TextField notes
        DateTimeField created_at
    }

    Directorate {
        UUID id PK
        CharField name
        TextField description
        UUID director_id FK
        DateTimeField created_at
    }

    Department {
        UUID id PK
        CharField name
        TextField description
        UUID directorate_id FK
        UUID hod_id FK
        UUID assistant_hod_id FK
        DateTimeField created_at
    }

    DepartmentMembership {
        UUID id PK
        UUID member_id FK
        UUID department_id FK
        DateField joined_at
        BooleanField is_active
    }

    Unit {
        UUID id PK
        CharField name
        TextField description
        UUID department_id FK
        UUID unit_head_id FK
        DateTimeField created_at
    }

    UnitMembership {
        UUID id PK
        UUID member_id FK
        UUID unit_id FK
        DateField joined_at
        BooleanField is_active
        CharField role
    }

    ServiceType {
        UUID id PK
        CharField name
        TextField description
        BooleanField is_recurring
    }

    Service {
        UUID id PK
        CharField name
        CharField theme
        CharField location
        UUID service_type_id FK
        DateTimeField created_at
    }

    Attendance {
        UUID id PK
        UUID member_id FK
        UUID service_id FK
        CharField service_type
        CharField connect_name
        CharField checkin_code
        DateField service_date
        DateTimeField created_at
    }

    ConnectGroup {
        UUID id PK
        UUID service_id FK
        CharField name
        TextField description
        CharField meeting_day
        CharField meeting_time
        DateTimeField created_at
    }

    ConnectGroupMember {
        UUID id PK
        UUID connect_group_id FK
        UUID member_id FK
        DateField joined_at
        DateField left_at
    }

    Pastor {
        UUID id PK
        CharField first_name
        CharField last_name
        CharField phone
        EmailField email
    }

    ConnectGroupPastor {
        UUID id PK
        UUID connect_group_id FK
        UUID pastor_id FK
        DateField start_date
        DateField end_date
    }

    Event {
        UUID id PK
        UUID service_id FK
        CharField event_type
        TextField description
        DateTimeField created_at
    }

    EventParticipation {
        UUID id PK
        UUID event_id FK
        UUID member_id FK
        CharField participant_name
        CharField role
    }

    GrowthTrack {
        UUID id PK
        CharField cohort_name
        DateField start_date
        DateField end_date
        CharField status
        DateTimeField created_at
    }

    GrowthTrackEnrollment {
        UUID id PK
        UUID growth_track_id FK
        UUID member_id FK
        DateField enrollment_date
        CharField status
        DateField graduation_date
    }

    Member ||--o{ FirstTimers : "first_timer_records"
    Service ||--o{ FirstTimers : "first_timers"
    Member ||--o{ Attendance : "attendances"
    Service ||--o{ Attendance : "attendances"
    Directorate ||--o{ Department : "departments"
    Member ||--o{ Directorate : "directorates_led"
    Member ||--o{ Department : "departments_led"
    Member ||--o{ Department : "departments_assisted"
    Department ||--o{ DepartmentMembership : "memberships"
    Member ||--o{ DepartmentMembership : "department_memberships"
    Department ||--o{ Unit : "units"
    Member ||--o{ Unit : "units_led"
    Unit ||--o{ UnitMembership : "memberships"
    Member ||--o{ UnitMembership : "unit_memberships"
    ServiceType ||--o{ Service : "services"
    Service ||--o{ ConnectGroup : "connect_groups"
    ConnectGroup ||--o{ ConnectGroupMember : "members"
    Member ||--o{ ConnectGroupMember : "connect_group_memberships"
    Pastor ||--o{ ConnectGroupPastor : "connect_groups"
    ConnectGroup ||--o{ ConnectGroupPastor : "pastor_assignments"
    Service ||--o{ Event : "events"
    Event ||--o{ EventParticipation : "participations"
    Member ||--o{ EventParticipation : "event_participations"
    GrowthTrack ||--o{ GrowthTrackEnrollment : "enrollments"
    Member ||--o{ GrowthTrackEnrollment : "growth_track_enrollments"
```

---

## Apps & Models Specification

### App: `apps.members`

#### Model: `Member` (Table: `members`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4, editable=False |
| `first_name` | `CharField` | — | max_length=100 |
| `last_name` | `CharField` | — | max_length=100 |
| `phone_number` | `CharField` | — | max_length=32, unique=True |
| `email` | `EmailField` | — | unique=True, null=True, blank=True |
| `gender` | `CharField` | — | max_length=32, null=True, blank=True |
| `birthday` | `YearlessDateField` | — | null=True, blank=True |
| `date_of_birth` | `DateField` | — | null=True, blank=True |
| `marital_status` | `CharField` | — | max_length=32, null=True, blank=True |
| `employment_status` | `CharField` | — | max_length=32, null=True, blank=True |
| `address` | `CharField` | — | max_length=255, null=True, blank=True |
| `is_worker` | `BooleanField` | — | default=False |
| `member_status` | `CharField` | — | default="regular_member" |
| `date_joined` | `DateTimeField` | — | null=True, blank=True |
| `created_at` | `DateTimeField` | — | auto_now_add=True |
| `updated_at` | `DateTimeField` | — | auto_now=True |

#### Model: `FirstTimers` (Table: `first_timer_events`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4, editable=False |
| `member` | `ForeignKey` | `Member` | on_delete=CASCADE, related_name="first_timer_records" |
| `service` | `ForeignKey` | `Service` | on_delete=SET_NULL, null=True, blank=True |
| `service_name` | `CharField` | — | max_length=200 |
| `service_date` | `DateField` | — |  |
| `service_type` | `CharField` | — | max_length=50, null=True, blank=True |
| `heard_about_church` | `CharField` | — | max_length=50, null=True, blank=True |
| `heard_about_church_other` | `CharField` | — | max_length=200, null=True, blank=True |
| `purpose_of_attending` | `TextField` | — | null=True, blank=True |
| `would_like_to_be_member` | `CharField` | — | max_length=20, null=True, blank=True |
| `invited_by` | `CharField` | — | max_length=150, null=True, blank=True |
| `follow_up_status` | `CharField` | — | default="pending" |
| `notes` | `TextField` | — | null=True, blank=True |
| `created_at` | `DateTimeField` | — | auto_now_add=True |

---

### App: `apps.departments`

#### Model: `Directorate` (Table: `directorate`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `name` | `CharField` | — | max_length=150, unique=True |
| `description` | `TextField` | — | blank=True |
| `director` | `ForeignKey` | `Member` | null=True, blank=True, on_delete=SET_NULL |
| `created_at` | `DateTimeField` | — | auto_now_add=True |

#### Model: `Department` (Table: `department`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `name` | `CharField` | — | max_length=150, unique=True |
| `description` | `TextField` | — | blank=True |
| `directorate` | `ForeignKey` | `Directorate` | null=True, blank=True, on_delete=CASCADE |
| `hod` | `ForeignKey` | `Member` | null=True, blank=True, on_delete=SET_NULL |
| `assistant_hod` | `ForeignKey` | `Member` | null=True, blank=True, on_delete=SET_NULL |
| `created_at` | `DateTimeField` | — | auto_now_add=True |

#### Model: `DepartmentMembership` (Table: `department_memberships`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `member` | `ForeignKey` | `Member` | on_delete=CASCADE |
| `department` | `ForeignKey` | `Department` | on_delete=CASCADE |
| `joined_at` | `DateField` | — |  |
| `is_active` | `BooleanField` | — | default=True |

#### Model: `Unit` (Table: `units`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `name` | `CharField` | — | max_length=150 |
| `description` | `TextField` | — | blank=True |
| `department` | `ForeignKey` | `Department` | on_delete=CASCADE |
| `unit_head` | `ForeignKey` | `Member` | null=True, blank=True, on_delete=SET_NULL |
| `created_at` | `DateTimeField` | — | auto_now_add=True |

#### Model: `UnitMembership` (Table: `unit_memberships`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `member` | `ForeignKey` | `Member` | on_delete=CASCADE |
| `unit` | `ForeignKey` | `Unit` | on_delete=CASCADE |
| `joined_at` | `DateField` | — |  |
| `is_active` | `BooleanField` | — | default=True |
| `role` | `CharField` | — | max_length=100, blank=True |

---

### App: `apps.services`

#### Model: `ServiceType` (Table: `service_types`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `name` | `CharField` | — | max_length=100 |
| `description` | `TextField` | — | blank=True |
| `is_recurring` | `BooleanField` | — | default=False |

#### Model: `Service` (Table: `service`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `name` | `CharField` | — | max_length=100 |
| `theme` | `CharField` | — | max_length=255, null=True, blank=True |
| `location` | `CharField` | — | max_length=255, null=True, blank=True |
| `service_type` | `ForeignKey` | `ServiceType` | null=True, blank=True, on_delete=SET_NULL |
| `created_at` | `DateTimeField` | — | auto_now_add=True |

---

### App: `apps.attendance`

#### Model: `Attendance` (Table: `attendance`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `member` | `ForeignKey` | `Member` | on_delete=CASCADE |
| `service` | `ForeignKey` | `Service` | on_delete=SET_NULL, null=True, blank=True |
| `service_type` | `CharField` | — | max_length=32 |
| `connect_name` | `CharField` | — | max_length=80, null=True, blank=True |
| `checkin_code` | `CharField` | — | max_length=32, unique=True, null=True, blank=True |
| `service_date` | `DateField` | — |  |
| `created_at` | `DateTimeField` | — | auto_now_add=True |

---

### App: `apps.connect_groups`

#### Model: `ConnectGroup` (Table: `connect_group`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `service` | `ForeignKey` | `Service` | on_delete=SET_NULL, null=True, blank=True |
| `name` | `CharField` | — | max_length=150 |
| `description` | `TextField` | — | blank=True |
| `meeting_day` | `CharField` | — | max_length=20 |
| `meeting_time` | `CharField` | — | max_length=80, blank=True |
| `created_at` | `DateTimeField` | — | auto_now_add=True |

#### Model: `ConnectGroupMember` (Table: `connect_group_members`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `connect_group` | `ForeignKey` | `ConnectGroup` | on_delete=CASCADE |
| `member` | `ForeignKey` | `Member` | on_delete=CASCADE |
| `joined_at` | `DateField` | — | auto_now_add=True |
| `left_at` | `DateField` | — | null=True, blank=True |

#### Model: `ConnectGroupPastor` (Table: `connect_group_pastors`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `connect_group` | `ForeignKey` | `ConnectGroup` | on_delete=CASCADE |
| `pastor` | `ForeignKey` | `Pastor` | on_delete=CASCADE |
| `start_date` | `DateField` | — |  |
| `end_date` | `DateField` | — | null=True, blank=True |

---

### App: `apps.pastors`

#### Model: `Pastor` (Table: `pastors`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `first_name` | `CharField` | — | max_length=100 |
| `last_name` | `CharField` | — | max_length=100 |
| `phone` | `CharField` | — | max_length=20 |
| `email` | `EmailField` | — | unique=True |

---

### App: `apps.events`

#### Model: `Event` (Table: `events`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `service` | `ForeignKey` | `Service` | on_delete=CASCADE |
| `event_type` | `CharField` | — | max_length=100 |
| `description` | `TextField` | — | blank=True |
| `created_at` | `DateTimeField` | — | auto_now_add=True |

#### Model: `EventParticipation` (Table: `event_participations`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `event` | `ForeignKey` | `Event` | on_delete=CASCADE |
| `member` | `ForeignKey` | `Member` | null=True, blank=True, on_delete=SET_NULL |
| `participant_name` | `CharField` | — | max_length=255 |
| `role` | `CharField` | — | max_length=100 |

---

### App: `apps.growth_track`

#### Model: `GrowthTrack` (Table: `growth_tracks`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `cohort_name` | `CharField` | — | max_length=100 |
| `start_date` | `DateField` | — |  |
| `end_date` | `DateField` | — |  |
| `status` | `CharField` | — | choices=["planned", "ongoing", "completed"] |
| `created_at` | `DateTimeField` | — | auto_now_add=True |

#### Model: `GrowthTrackEnrollment` (Table: `growth_track_enrollments`)
| Field Name | Type | Related Model | Attributes / Constraints |
| --- | --- | --- | --- |
| `id` | `UUIDField` | — | PK, default=uuid4 |
| `growth_track` | `ForeignKey` | `GrowthTrack` | on_delete=CASCADE |
| `member` | `ForeignKey` | `Member` | on_delete=CASCADE |
| `enrollment_date` | `DateField` | — |  |
| `status` | `CharField` | — | choices=["active", "completed", "dropped"] |
| `graduation_date` | `DateField` | — | null=True, blank=True |
