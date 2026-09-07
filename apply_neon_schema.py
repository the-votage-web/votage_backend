import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "church.settings")
django.setup()

from django.db import connection

def run_migration():
    with connection.cursor() as cur:
        print("1. Updating first_timer_events table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS first_timer_events (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                member_id UUID NOT NULL REFERENCES members(id) ON DELETE CASCADE,
                service_id UUID REFERENCES service(id) ON DELETE SET NULL,
                service_name VARCHAR(200) NOT NULL DEFAULT 'Sunday Service',
                service_date DATE NOT NULL DEFAULT CURRENT_DATE,
                service_type VARCHAR(50),
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );

            ALTER TABLE first_timer_events 
            ADD COLUMN IF NOT EXISTS heard_about_church VARCHAR(50),
            ADD COLUMN IF NOT EXISTS heard_about_church_other VARCHAR(200),
            ADD COLUMN IF NOT EXISTS purpose_of_attending TEXT,
            ADD COLUMN IF NOT EXISTS would_like_to_be_member VARCHAR(20),
            ADD COLUMN IF NOT EXISTS invited_by VARCHAR(150),
            ADD COLUMN IF NOT EXISTS follow_up_status VARCHAR(50) DEFAULT 'pending',
            ADD COLUMN IF NOT EXISTS notes TEXT;
        """)

        print("2. Migrating first-timer data from members to first_timer_events...")
        cur.execute("""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='members' AND column_name='heard_about_church'
                ) THEN
                    UPDATE first_timer_events fte
                    SET heard_about_church = m.heard_about_church,
                        heard_about_church_other = m.heard_about_church_other,
                        purpose_of_attending = m.purpose_of_attending,
                        would_like_to_be_member = m.would_like_to_be_member,
                        invited_by = m.connect_name
                    FROM members m
                    WHERE fte.member_id = m.id;
                END IF;
            END $$;
        """)

        print("3. Updating members table...")
        cur.execute("""
            ALTER TABLE members 
            ADD COLUMN IF NOT EXISTS member_status VARCHAR(32) DEFAULT 'regular_member',
            ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();

            ALTER TABLE members 
            DROP COLUMN IF EXISTS heard_about_church,
            DROP COLUMN IF EXISTS heard_about_church_other,
            DROP COLUMN IF EXISTS purpose_of_attending,
            DROP COLUMN IF EXISTS would_like_to_be_member,
            DROP COLUMN IF EXISTS first_timer,
            DROP COLUMN IF EXISTS connect_name;
        """)

        print("4. Creating / updating department and hierarchy tables...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS directorate (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR(150) UNIQUE NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                director_id UUID REFERENCES members(id) ON DELETE SET NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );

            ALTER TABLE department 
            ADD COLUMN IF NOT EXISTS description TEXT NOT NULL DEFAULT '',
            ADD COLUMN IF NOT EXISTS directorate_id UUID REFERENCES directorate(id) ON DELETE CASCADE,
            ADD COLUMN IF NOT EXISTS hod_id UUID REFERENCES members(id) ON DELETE SET NULL,
            ADD COLUMN IF NOT EXISTS assistant_hod_id UUID REFERENCES members(id) ON DELETE SET NULL;

            CREATE TABLE IF NOT EXISTS department_memberships (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                member_id UUID NOT NULL REFERENCES members(id) ON DELETE CASCADE,
                department_id UUID NOT NULL REFERENCES department(id) ON DELETE CASCADE,
                joined_at DATE NOT NULL DEFAULT CURRENT_DATE,
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                CONSTRAINT unique_member_department UNIQUE (member_id, department_id)
            );

            CREATE TABLE IF NOT EXISTS units (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR(150) NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                department_id UUID NOT NULL REFERENCES department(id) ON DELETE CASCADE,
                unit_head_id UUID REFERENCES members(id) ON DELETE SET NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                CONSTRAINT unique_unit_department UNIQUE (name, department_id)
            );

            CREATE TABLE IF NOT EXISTS unit_memberships (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                member_id UUID NOT NULL REFERENCES members(id) ON DELETE CASCADE,
                unit_id UUID NOT NULL REFERENCES units(id) ON DELETE CASCADE,
                joined_at DATE NOT NULL DEFAULT CURRENT_DATE,
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                role VARCHAR(100) NOT NULL DEFAULT '',
                CONSTRAINT unique_member_unit UNIQUE (member_id, unit_id)
            );
        """)

        print("5. Creating / updating service and attendance tables...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS service_types (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR(100) NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                is_recurring BOOLEAN NOT NULL DEFAULT FALSE
            );

            ALTER TABLE service 
            ADD COLUMN IF NOT EXISTS service_type_id UUID REFERENCES service_types(id) ON DELETE SET NULL;

            ALTER TABLE attendance 
            ADD COLUMN IF NOT EXISTS connect_name VARCHAR(80),
            ADD COLUMN IF NOT EXISTS checkin_code VARCHAR(32) UNIQUE;
        """)

        print("6. Creating / updating pastors and connect group tables...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pastors (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(254) UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS connect_group_pastors (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                connect_group_id UUID NOT NULL REFERENCES connect_group(id) ON DELETE CASCADE,
                pastor_id UUID NOT NULL REFERENCES pastors(id) ON DELETE CASCADE,
                start_date DATE NOT NULL DEFAULT CURRENT_DATE,
                end_date DATE
            );
        """)

        print("7. Creating / updating events and growth track tables...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                service_id UUID NOT NULL REFERENCES service(id) ON DELETE CASCADE,
                event_type VARCHAR(100) NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS event_participations (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
                member_id UUID REFERENCES members(id) ON DELETE SET NULL,
                participant_name VARCHAR(255) NOT NULL,
                role VARCHAR(100) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS growth_tracks (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                cohort_name VARCHAR(100) NOT NULL,
                start_date DATE NOT NULL DEFAULT CURRENT_DATE,
                end_date DATE NOT NULL DEFAULT CURRENT_DATE,
                status VARCHAR(20) NOT NULL DEFAULT 'planned',
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS growth_track_enrollments (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                growth_track_id UUID NOT NULL REFERENCES growth_tracks(id) ON DELETE CASCADE,
                member_id UUID NOT NULL REFERENCES members(id) ON DELETE CASCADE,
                enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
                status VARCHAR(20) NOT NULL DEFAULT 'active',
                graduation_date DATE,
                CONSTRAINT unique_growth_track_enrollment UNIQUE (growth_track_id, member_id)
            );
        """)

    print("Migration successfully applied to Neon Postgres!")

if __name__ == "__main__":
    run_migration()
