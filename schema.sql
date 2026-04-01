-- ============================================================
-- Student Record Management System — Database Schema
-- Run this in your Supabase SQL Editor
-- ============================================================

-- 1. USERS (Admin accounts)
CREATE TABLE IF NOT EXISTS users (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(50)  UNIQUE NOT NULL,
    email         VARCHAR(100) UNIQUE,
    full_name     VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. CLASSES
CREATE TABLE IF NOT EXISTS classes (
    id         SERIAL PRIMARY KEY,
    class_name VARCHAR(20)  NOT NULL,
    teacher_id INT,
    year       VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. TEACHERS
CREATE TABLE IF NOT EXISTS teachers (
    id             SERIAL PRIMARY KEY,
    first_name     VARCHAR(50)  NOT NULL,
    last_name      VARCHAR(50),
    email          VARCHAR(100),
    phone_no       VARCHAR(15),
    specialization VARCHAR(100),
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. COURSES
CREATE TABLE IF NOT EXISTS courses (
    id           SERIAL PRIMARY KEY,
    course_name  VARCHAR(100) NOT NULL,
    course_code  VARCHAR(30)  UNIQUE,
    credit_hours INT,
    description  VARCHAR(200),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. STUDENTS (Core table)
CREATE TABLE IF NOT EXISTS students (
    id                SERIAL PRIMARY KEY,
    first_name        VARCHAR(50)  NOT NULL,
    last_name         VARCHAR(50),
    roll_no           VARCHAR(30)  UNIQUE NOT NULL,
    gender            VARCHAR(10),
    dob               DATE,
    email             VARCHAR(100),
    phone_no          VARCHAR(15),
    address           VARCHAR(150),
    guardian_name     VARCHAR(100),
    guardian_contact  VARCHAR(15),
    department        VARCHAR(100),
    class_id          INT REFERENCES classes(id) ON DELETE SET NULL,
    admission_date    DATE,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. SUBJECTS
CREATE TABLE IF NOT EXISTS subjects (
    id           SERIAL PRIMARY KEY,
    subject_name VARCHAR(50) NOT NULL,
    class_id     INT REFERENCES classes(id) ON DELETE SET NULL,
    teacher_id   INT REFERENCES teachers(id) ON DELETE SET NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. ENROLLMENT
CREATE TABLE IF NOT EXISTS enrollment (
    id            SERIAL PRIMARY KEY,
    student_id    INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id     INT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    enroll_date   DATE,
    status        VARCHAR(20) DEFAULT 'Active',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. EXAMS
CREATE TABLE IF NOT EXISTS exams (
    id        SERIAL PRIMARY KEY,
    course_id INT REFERENCES courses(id) ON DELETE SET NULL,
    exam_date DATE,
    exam_type VARCHAR(80),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. RESULTS
CREATE TABLE IF NOT EXISTS results (
    id              SERIAL PRIMARY KEY,
    student_id      INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    exam_id         INT REFERENCES exams(id) ON DELETE SET NULL,
    subject_id      INT REFERENCES subjects(id) ON DELETE SET NULL,
    marks_obtained  INT,
    grade           VARCHAR(5),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. ATTENDANCE
CREATE TABLE IF NOT EXISTS attendance (
    id            SERIAL PRIMARY KEY,
    student_id    INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id     INT REFERENCES courses(id) ON DELETE SET NULL,
    date          DATE,
    status        VARCHAR(10),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. FEES
CREATE TABLE IF NOT EXISTS fees (
    id              SERIAL PRIMARY KEY,
    student_id      INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    amount          NUMERIC(10,2),
    payment_date    DATE,
    payment_method  VARCHAR(80),
    payment_status  VARCHAR(20) DEFAULT 'Pending',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- SEED: Default admin user (password: admin123)
-- ============================================================
INSERT INTO users (username, email, full_name, password_hash)
VALUES (
    'admin',
    'admin@vcacs.edu',
    'System Administrator',
    'scrypt:32768:8:1$salt$hash'  -- Replace with actual hash or run seed.py
)
ON CONFLICT (username) DO NOTHING;

-- SEED: Sample classes
INSERT INTO classes (class_name, year) VALUES
    ('SY BSc CS', '2024'),
    ('TY BSc CS', '2024'),
    ('FY BSc IT', '2024'),
    ('SY BCA',    '2024')
ON CONFLICT DO NOTHING;
